"""Solve a lesson non-interactively and report pass/fail and keystroke count.

For lesson authors and CI. Keys are given as a Python bytes literal so that
control characters are unambiguous: \x1b is Esc, \r is Enter, \x16 is Ctrl-V.

    ./dojo verify 04-07 '3jdd:wq\r'
    ./dojo verify 10-04 'ci"localhost\x1b:wq\r'
"""
import ast
import subprocess
import sys
import tempfile
from pathlib import Path

from engine import ui
from engine.lesson import find, load_all
from engine.runner import Attempt


ESCAPES = {"r": b"\r", "n": b"\n", "t": b"\t", "e": b"\x1b", "\\": b"\\"}
HEX = "0123456789abcdefABCDEF"


def decode(spec):
    r"""Turn a keystroke spec into bytes.

    Only a handful of escapes mean anything here: \xHH, \r, \n, \t, \e (Esc)
    and \\ for a literal backslash. Every other backslash is passed through
    untouched, because it is almost certainly part of a vim pattern -- \C,
    \<, \(, \1 -- and Python's own escape rules would quietly turn \1 into
    a control character. A bytes literal (b'...') is also accepted as-is.
    """
    if spec.startswith(("b'", 'b"')):
        return ast.literal_eval(spec)
    out = bytearray()
    i = 0
    while i < len(spec):
        ch = spec[i]
        if ch != "\\" or i + 1 >= len(spec):
            out += ch.encode("utf-8")
            i += 1
            continue
        nxt = spec[i + 1]
        if nxt == "x" and len(spec) >= i + 4 and all(c in HEX for c in spec[i + 2:i + 4]):
            out.append(int(spec[i + 2:i + 4], 16))
            i += 4
        elif nxt in ESCAPES:
            out += ESCAPES[nxt]
            i += 2
        else:
            out += b"\\" + nxt.encode("utf-8")
            i += 2
    return bytes(out)


def solve(lesson, keys, slow=False):
    att = Attempt(lesson)
    att.prepare(force=True)
    if slow:
        _solve_slow(att, keys)
    else:
        att.meta_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix=".keys", delete=False,
                                         dir=att.meta_dir) as fh:
            fh.write(keys)
            script = fh.name
        subprocess.call(att.command(script), cwd=att.dir,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        Path(script).unlink(missing_ok=True)
    passed, failures = att.check(verbose=False)
    return passed, failures, att.keystrokes(), att.used_arrows()


def _solve_slow(att, keys, pause=0.25):
    """Type through a pty, pausing after Esc and Enter.

    `vim -s` never idles, and vim only closes an undo block when it idles
    waiting for input, so under -s every insert session merges into one undo
    step and lessons about u, U, Ctrl-R, :earlier or g- cannot be checked.
    A pty with short pauses reproduces what a human's fingers do.
    """
    import os
    import pty
    import select
    import time

    pid, fd = pty.fork()
    if pid == 0:
        os.environ["TERM"] = "xterm"
        os.chdir(att.dir)
        os.execvp("vim", att.command())
    def drain(seconds):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            r, _, _ = select.select([fd], [], [], 0.02)
            if r:
                try:
                    os.read(fd, 65536)
                except OSError:
                    return
    drain(0.6)
    for b in keys:
        os.write(fd, bytes([b]))
        drain(pause if b in (0x1b, 0x0d) else 0.01)
    drain(0.5)
    try:
        os.waitpid(pid, 0)
    except ChildProcessError:
        pass
    os.close(fd)


def run(args):
    slow = "--slow" in args
    args = [a for a in args if a != "--slow"]
    if len(args) < 2:
        print("\n  usage: ./dojo verify [--slow] <lesson-id> '<keystrokes>'")
        print("  e.g.   ./dojo verify 01-01 'iDaily \\x1b:wq\\r'")
        print("  --slow types through a terminal with pauses; needed for undo lessons\n")
        return 1
    l = find(args[0])
    if not l:
        print(f"\n  no lesson '{args[0]}'\n")
        return 1
    keys = decode(args[1])
    passed, failures, count, arrows = solve(l, keys, slow=slow)

    mark = f"{ui.GRN}PASS{ui.R}" if passed else f"{ui.RED}FAIL{ui.R}"
    over = count > l.par
    budget = (f"{ui.RED}{count} > par {l.par}{ui.R}" if over
              else f"{ui.GRN}{count} <= par {l.par}{ui.R}")
    print(f"\n  {mark}  {l.id} {l.title}")
    print(f"        keystrokes {budget}"
          + (f"   {ui.YEL}arrow keys or mouse used{ui.R}" if arrows else ""))
    for f in failures:
        print(f"        {ui.RED}·{ui.R} {f}")
    print()
    return 0 if (passed and not over) else 1
