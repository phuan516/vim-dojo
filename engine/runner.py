"""Running a lesson: materialise files, drive vim, grade the result."""
import difflib
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from engine import ui
from engine.lesson import Lesson

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / ".dojo" / "work"
KEYLOG = ROOT / ".dojo" / "keys.log"  # legacy shared path; no longer read or written

# Vim writes special keys into a -w keylog as 0x80 followed by two more
# bytes. Exactly one of those is produced by ordinary keyboard editing:
# K_IGNORE (\x80\xfd5), which vim emits after a character-pending read such
# as f, t, r or R. Verified by running a battery of normal-mode editing --
# operators, text objects, search, visual, macros, marks, substitute, undo,
# counts, replace, indent -- and finding no other special sequence at all.
#
# So: strip K_IGNORE, and anything 0x80-prefixed still left is an arrow key,
# a navigation key or the mouse. That rule needs no table of terminal codes
# and does not go stale.
K_IGNORE = b"\x80\xfd5"   # vim bookkeeping after f/t/r/R — not a key press at all
K_BS = b"\x80kb"          # Backspace — a real key press, and a perfectly fair one


def real_keys(log):
    """The keylog reduced to what the player actually pressed.

    K_IGNORE disappears: vim emitted it, not the player. Backspace collapses
    to one byte so a single press costs one keystroke rather than three, and
    so it is not mistaken for an arrow key. Whatever 0x80 survives this is a
    cursor key, a navigation key or the mouse.
    """
    return log.replace(K_IGNORE, b"").replace(K_BS, b"\x08")


def normalise(text):
    """Trailing whitespace and a missing final newline are never the lesson."""
    lines = [l.rstrip() for l in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines) + "\n"


class Attempt:
    """One go at a lesson. Everything it produces lives under its own directory.

    The keystroke log, vim's undo history and its viminfo all live inside the
    attempt directory rather than anywhere shared, so two attempts can never
    read each other's keys, a replay never inherits the undo tree of the
    attempt it replaced, and the jumplist starts empty every time.
    """

    def __init__(self, lesson):
        self.lesson = lesson
        self.dir = WORK / lesson.slug
        self.seconds = None

    @property
    def meta_dir(self):
        """Harness files, kept OUT of the work directory.

        The work directory is vim's cwd, so anything in it is visible to the
        lesson: netrw lists it, `:find` completes it, and `:grep -r pat .`
        matches the keystroke script and then `:cdo` edits it mid-read. The
        player's directory contains only the lesson's own files.
        """
        return self.dir.parent / ".harness" / self.dir.name

    @property
    def keylog(self):
        return self.meta_dir / "keys.log"

    @property
    def undodir(self):
        return self.meta_dir / "undo"

    @property
    def viminfo(self):
        return self.meta_dir / "viminfo"

    @property
    def swapdir(self):
        return self.meta_dir / "swap"

    # ---------- setup ----------
    def prepare(self, force=False):
        if force:
            for d in (self.dir, self.meta_dir):
                if d.exists():
                    shutil.rmtree(d)
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        if not self.dir.exists():
            self.dir.mkdir(parents=True)
            for name, content in self.lesson.start.items():
                p = self.dir / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content, encoding="utf-8")
        return self.dir

    def wipe(self):
        for d in (self.dir, self.meta_dir):
            if d.exists():
                shutil.rmtree(d)

    # ---------- vim ----------
    def command(self, script=None):
        """The vim invocation for this attempt. `script` adds -s for non-interactive runs."""
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        self.keylog.unlink(missing_ok=True)
        self.undodir.mkdir(parents=True, exist_ok=True)
        self.swapdir.mkdir(parents=True, exist_ok=True)
        files = list(self.lesson.open_files)
        for f in files:
            (self.dir / f).parent.mkdir(parents=True, exist_ok=True)
        # -i keeps the jumplist, changelist, marks and registers private to
        # this attempt. Without it vim seeds them from ~/.viminfo, so a jump
        # lesson behaves differently on every machine and Ctrl-O can walk off
        # into a file from last week -- and the dojo's scratch files end up in
        # the player's own history.
        # clipboard= keeps the unnamed register inside this vim. The player's
        # own vimrc may set clipboard=unnamedplus, which makes y and p go
        # through the real system clipboard -- so a plain p could put whatever
        # another program copied a moment ago, and a graded lesson would depend
        # on the state of the desktop. An explicit "+ or "* still reaches the
        # system clipboard, so the lessons that teach it work unchanged; one
        # that genuinely needs the integration can set it back through `vimrc`.
        cmd = ["vim", "-w", str(self.keylog), "-i", str(self.viminfo),
               "-c", f"set undodir={self.undodir}",
               "-c", f"set directory={self.swapdir}//",
               "-c", "set clipboard="]
        if script:
            cmd += ["-s", str(script)]
        rc_extra = self.lesson.meta.get("vimrc")
        if rc_extra:
            cmd += ["-c", rc_extra]
        return cmd + files

    def launch(self):
        cmd = self.command()
        started = time.monotonic()
        subprocess.call(cmd, cwd=self.dir)
        self.seconds = round(time.monotonic() - started, 1)

    # ---------- measurement ----------
    def _log(self):
        return self.keylog.read_bytes() if self.keylog.exists() else b""

    def keystrokes(self):
        """Bytes the player actually pressed.

        K_IGNORE is vim's own bookkeeping, not a key, so `f,` costs two and
        not five. Without this every lesson built on find motions would be
        silently over-charged.
        """
        return len(real_keys(self._log()))

    def used_arrows(self):
        """Did they reach for the arrow keys, the navigation block, or the mouse?"""
        return b"\x80" in real_keys(self._log())

    # ---------- grading ----------
    def check(self, verbose=True):
        if not self.dir.exists():
            return None, ["nothing to check — run ./dojo play first"]

        failures = []
        for name, want in sorted(self.lesson.expected.items()):
            got_path = self.dir / name
            if not got_path.exists():
                failures.append(f"{name}: you never created this file")
                if verbose:
                    print(f"  {ui.RED}✘{ui.R} {name}  {ui.D}missing{ui.R}")
                continue
            got = normalise(got_path.read_text(encoding="utf-8", errors="replace"))
            exp = normalise(want)
            if got == exp:
                if verbose:
                    print(f"  {ui.GRN}✔{ui.R} {name}")
                continue
            failures.append(name)
            if verbose:
                print(f"  {ui.RED}✘{ui.R} {name}")
                self._show_diff(exp, got)

        # Files given in @start with no @expected twin must be left alone.
        for name in self.lesson.start:
            if name in self.lesson.expected:
                continue
            p = self.dir / name
            if not p.exists():
                failures.append(f"{name}: deleted, but this file was not yours to touch")
            elif normalise(p.read_text(encoding="utf-8", errors="replace")) != normalise(
                self.lesson.start[name]
            ):
                failures.append(f"{name}: changed, but this file was not yours to touch")
                if verbose:
                    print(f"  {ui.RED}✘{ui.R} {name}  {ui.D}should have been left untouched{ui.R}")

        return (len(failures) == 0), failures

    @staticmethod
    def _show_diff(expected, got, limit=24):
        diff = difflib.unified_diff(
            expected.splitlines(), got.splitlines(),
            fromfile="expected", tofile="yours", lineterm="", n=1,
        )
        shown = 0
        for line in diff:
            if shown >= limit:
                print(f"      {ui.D}… diff truncated{ui.R}")
                break
            if line.startswith("+++") or line.startswith("---"):
                continue
            if line.startswith("@@"):
                print(f"      {ui.D}{line}{ui.R}")
            elif line.startswith("-"):
                print(f"      {ui.GRN}want {ui.R}{line[1:]}")
            elif line.startswith("+"):
                print(f"      {ui.RED}got  {ui.R}{line[1:]}")
            else:
                continue
            shown += 1
