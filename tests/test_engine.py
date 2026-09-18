"""Engine tests. Run with: python3 -m tests.test_engine

No pytest dependency on purpose — the dojo should need nothing but python3
and vim, on any machine the player sits down at.
"""
import shutil
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.lesson import Lesson, LessonError  # noqa: E402
from engine.runner import Attempt, normalise  # noqa: E402
from engine.state import State  # noqa: E402

PASSED, FAILED = [], []


def check(name, cond, detail=""):
    (PASSED if cond else FAILED).append(name)
    mark = "ok  " if cond else "FAIL"
    print(f"  {mark} {name}" + (f"  — {detail}" if detail and not cond else ""))


def write_lesson(tmp, body):
    p = Path(tmp) / "99-01-test.lesson"
    p.write_text(body, encoding="utf-8")
    return p


MINIMAL = """@meta
id: 99-01
title: A test lesson
chapter: 99
type: lesson
skills: alpha, beta
par: 20
open: a.txt

@brief
Do the thing.

@keys
| `x` | delete a character |

@hints
First.
--
Second.

@solution
Press x.

@start a.txt
hello
untouched

@expected a.txt
hell
untouched
"""


# ---------------------------------------------------------------- parsing
def test_parsing():
    with tempfile.TemporaryDirectory() as tmp:
        l = Lesson(write_lesson(tmp, MINIMAL))
        check("parses meta", l.title == "A test lesson")
        check("parses id", l.id == "99-01")
        check("splits skills", l.skills == ["alpha", "beta"])
        check("par is an int", l.par == 20)
        check("splits hints on --", len(l.hints) == 2, f"got {len(l.hints)}")
        check("reads start file", l.start["a.txt"].startswith("hello"))
        check("reads expected file", l.expected["a.txt"].startswith("hell\n"))
        check("open_files honours meta", l.open_files == ["a.txt"])
        check("default type is lesson", l.type == "lesson")
    macro = MINIMAL.replace("Press x.", "Press x, then @a to replay it.\n@a\n@injectable()")
    with tempfile.TemporaryDirectory() as tmp:
        l = Lesson(write_lesson(tmp, macro))
        check("@a is content, not a section", "@a" in l.solution, repr(l.solution[-40:]))
        check("@injectable() is content", "@injectable()" in l.solution)
    escaped = MINIMAL.replace("@start a.txt\nhello", "@start a.txt\n\\@start\nhello")
    with tempfile.TemporaryDirectory() as tmp:
        l = Lesson(write_lesson(tmp, escaped))
        check("\\@ escapes a real section name", l.start["a.txt"].startswith("@start\n"),
              repr(l.start["a.txt"][:12]))


def test_validation():
    cases = {
        "missing title": MINIMAL.replace("title: A test lesson\n", ""),
        "missing skills": MINIMAL.replace("skills: alpha, beta\n", ""),
        "non-numeric par": MINIMAL.replace("par: 20", "par: lots"),

        "bad type": MINIMAL.replace("type: lesson", "type: quiz"),
        "no expected": MINIMAL.split("@expected")[0],
    }
    with tempfile.TemporaryDirectory() as tmp:
        for name, body in cases.items():
            try:
                Lesson(write_lesson(tmp, body))
                check(f"rejects {name}", False, "no error raised")
            except LessonError:
                check(f"rejects {name}", True)


def test_find_surfaces_broken_files():
    """A typo'd section must not make a lesson silently disappear."""
    from engine import lesson as L
    # Point discovery at a private directory so this never races with a
    # `./dojo doctor` run by someone else against the real lessons tree.
    real = L.LESSONS
    with tempfile.TemporaryDirectory() as tmp:
        L.LESSONS = Path(tmp)
        try:
            broken_dir = L.LESSONS / "99-zz-test-only"
            broken_dir.mkdir()
            (broken_dir / "99-01-broken.lesson").write_text(
                MINIMAL.replace("par: 20", "par: not-a-number"))
            try:
                L.find("99-01")
                check("find raises for a broken file", False, "returned without error")
            except L.LessonError as e:
                check("find raises for a broken file", "par must be" in str(e), str(e))
            check("find returns None for a real absence", L.find("no-such-lesson-xyz") is None)
        finally:
            L.LESSONS = real


def test_verify_decode():
    """Keystroke specs must not mangle vim patterns."""
    from engine.verify import decode
    cases = {
        r"iDaily \x1b:wq\r": b"iDaily \x1b:wq\r",
        r"/\Cerror\r": b"/\\Cerror\r",
        r"/\<id\>\r": b"/\\<id\\>\r",
        r":%s/\(\w\+\)/\1/g\r": b":%s/\\(\\w\\+\\)/\\1/g\r",
        r"a\tb\n": b"a\tb\n",
        r"i\e": b"i\x1b",
        r"\\": b"\\",
        r"\x16jI#\x1b": b"\x16jI#\x1b",
        "b'raw\\x1b'": b"raw\x1b",
    }
    for spec, want in cases.items():
        got = decode(spec)
        check(f"decode {spec!r}", got == want, f"got {got!r}")


# ---------------------------------------------------------------- grading
def test_normalise():
    check("trailing spaces ignored", normalise("a   \nb\n") == normalise("a\nb\n"))
    check("missing final newline ignored", normalise("a\nb") == normalise("a\nb\n"))
    check("extra blank lines at EOF ignored", normalise("a\n\n\n") == normalise("a\n"))
    check("real differences survive", normalise("a\n") != normalise("b\n"))
    check("crlf normalised", normalise("a\r\nb\r\n") == normalise("a\nb\n"))


def test_isolation():
    """Two attempts must never see each other's keystrokes or undo history."""
    with tempfile.TemporaryDirectory() as tmp:
        l = Lesson(write_lesson(tmp, MINIMAL))
        a, b = Attempt(l), Attempt(l)
        a.dir, b.dir = Path(tmp) / "a", Path(tmp) / "b"
        a.prepare(); b.prepare()
        a.keylog.write_bytes(b"x" * 40)
        check("attempts have separate keylogs", b.keystrokes() == 0, str(b.keystrokes()))
        check("keylog is outside the work directory", a.dir not in a.keylog.parents)
        check("undo history is outside the work directory", a.dir not in a.undodir.parents)
        cmd = a.command()
        check("vim is told where undo goes", any(str(a.undodir) in c for c in cmd))
        check("vim logs keys to the attempt", str(a.keylog) in cmd)
        check("viminfo is private to the attempt", str(a.viminfo) in cmd)
        check("unnamed register is not the system clipboard",
              "set clipboard=" in cmd)
        check("swap files are outside the work directory",
              any(str(a.swapdir) in c for c in cmd) and a.dir not in a.swapdir.parents)
        check("viminfo is outside the work directory", a.dir not in a.viminfo.parents)
        a.keylog.write_bytes(b"x")
        visible = sorted(p.name for p in a.dir.iterdir())
        check("work dir holds only lesson files", visible == ["a.txt"], str(visible))
        a.wipe()
        check("wipe removes the keylog with the attempt", not a.keylog.exists())


def test_checking():
    with tempfile.TemporaryDirectory() as tmp:
        l = Lesson(write_lesson(tmp, MINIMAL))
        att = Attempt(l)
        att.dir = Path(tmp) / "work"
        att.prepare(force=True)

        ok, fails = att.check(verbose=False)
        check("unedited start file fails", not ok)

        (att.dir / "a.txt").write_text("hell\nuntouched\n")
        ok, fails = att.check(verbose=False)
        check("correct edit passes", ok, str(fails))

        (att.dir / "a.txt").write_text("hell\nuntouched   \n\n")
        ok, _ = att.check(verbose=False)
        check("whitespace-only noise still passes", ok)

        (att.dir / "a.txt").unlink()
        ok, fails = att.check(verbose=False)
        check("deleted file fails", not ok and "never created" in fails[0])
        att.wipe()


def test_decoy_files():
    body = MINIMAL + "\n@start decoy.txt\nleave me alone\n"
    with tempfile.TemporaryDirectory() as tmp:
        l = Lesson(write_lesson(tmp, body))
        att = Attempt(l)
        att.dir = Path(tmp) / "work"
        att.prepare(force=True)
        (att.dir / "a.txt").write_text("hell\nuntouched\n")

        ok, _ = att.check(verbose=False)
        check("decoy left alone passes", ok)

        (att.dir / "decoy.txt").write_text("meddled\n")
        ok, fails = att.check(verbose=False)
        check("editing a decoy fails", not ok and "not yours to touch" in fails[0], str(fails))

        (att.dir / "decoy.txt").unlink()
        ok, fails = att.check(verbose=False)
        check("deleting a decoy fails", not ok, str(fails))
        att.wipe()


# ---------------------------------------------------------------- arrows
def _probe():
    """An Attempt whose keylog we can write directly."""
    with tempfile.TemporaryDirectory() as tmp:
        l = Lesson(write_lesson(tmp, MINIMAL))
    att = Attempt(l)
    att.dir = Path(tempfile.mkdtemp()) / "work"
    att.meta_dir.mkdir(parents=True, exist_ok=True)
    return att


def test_arrow_detection():
    """What counts as reaching for the mouse, and what a key press costs."""
    att = _probe()
    # (name, keylog bytes, should flag as arrows/mouse, keystrokes charged)
    cases = [
        ("clean run",        b"ciwhi\x1b:wq\r",         False, 10),
        # vim emits K_IGNORE after a character-pending read; the player did not
        # press it, so f/t/r must not be charged for it
        ("f then edit",      b"f,\x80\xfd5i!\x1b:wq\r", False, 9),
        ("t then edit",      b"t)\x80\xfd5i!\x1b:wq\r", False, 9),
        ("replace r",        b"rx\x80\xfd5:wq\r",       False, 6),
        # backspace is a fair key: one press, one keystroke, no penalty
        ("backspace",        b"iab\x80kb\x1b",          False, 5),
        # the arrow tax: flagged, and still charged three bytes a press
        ("left arrow",       b"i\x80kl\x1b",            True,  5),
        ("two down arrows",  b"\x80kd\x80kddd",         True,  8),
        ("page down",        b"\x80kN",                 True,  3),
        ("home key",         b"\x80kh",                 True,  3),
        ("mouse click",      b"\x80\xfd\x2d",           True,  3),
    ]
    for name, log, want_flag, want_keys in cases:
        att.keylog.write_bytes(log)
        check(f"arrows: {name}", att.used_arrows() is want_flag,
              f"flag was {att.used_arrows()}")
        check(f"cost: {name}", att.keystrokes() == want_keys,
              f"charged {att.keystrokes()}, wanted {want_keys}")
    shutil.rmtree(att.dir.parent)


def test_arrow_tax_is_real():
    """The premise of lesson 03-11: arrowing is about three times the price."""
    att = _probe()
    att.keylog.write_bytes(b"jA,\x1b" * 5)
    hjkl = att.keystrokes()
    att.keylog.write_bytes(b"\x80kd\x80@7,\x1b" * 5)
    arrows = att.keystrokes()
    check("arrowing costs meaningfully more", arrows > hjkl * 1.5,
          f"{arrows} vs {hjkl}")
    shutil.rmtree(att.dir.parent)


# ---------------------------------------------------------------- state
class FakeLesson:
    def __init__(self, par=20, skills=("alpha",)):
        self.slug = "99-01-test"
        self.par = par
        self.skills = list(skills)


def test_grading_curve():
    L = FakeLesson(par=20)
    check("failure grades 1", State.grade(L, False, 40, False) == 1)
    check("under par grades 5", State.grade(L, True, 18, False) == 5)
    check("a bit over grades 4", State.grade(L, True, 28, False) == 4)
    check("well over grades 3", State.grade(L, True, 45, False) == 3)
    check("way over grades 2", State.grade(L, True, 90, False) == 2)
    check("arrows cost a grade", State.grade(L, True, 18, True) == 4)
    check("arrows never push below 2", State.grade(L, True, 90, True) == 2)


def test_srs():
    with tempfile.TemporaryDirectory() as tmp:
        s = State(Path(tmp) / "state.json")
        L = FakeLesson()

        s.record_attempt(L, True, 15, False)
        first = s.data["skills"]["alpha"]
        check("mastery rises on a clean pass", first["mastery"] > 0)
        check("first interval is short", first["interval"] <= 1, str(first["interval"]))

        for _ in range(3):
            s.record_attempt(L, True, 15, False)
        grown = dict(s.data["skills"]["alpha"])  # copy: the live dict mutates below
        check("interval grows with repeats", grown["interval"] > 2, str(grown["interval"]))
        check("mastery caps at 1.0", grown["mastery"] <= 1.0)
        due = date.fromisoformat(grown["due"])
        check("due date is in the future", due > date.today())

        s.record_attempt(L, False, 80, True)
        lapsed = s.data["skills"]["alpha"]
        check("a failure resets the interval", lapsed["interval"] == 0)
        check("a failure counts a lapse", lapsed["lapses"] == 1)
        check("a failure makes it due today", lapsed["due"] == date.today().isoformat())
        check("mastery drops on a failure", lapsed["mastery"] < grown["mastery"])
        check("ease never goes below the floor", lapsed["ease"] >= 1.3)


def test_personal_bests():
    with tempfile.TemporaryDirectory() as tmp:
        s = State(Path(tmp) / "state.json")
        L = FakeLesson(par=20)
        s.record_attempt(L, True, 30, False)
        check("best is recorded", s.lesson(L.slug)["best_keys"] == 30)
        s.record_attempt(L, True, 18, False)
        check("best improves", s.lesson(L.slug)["best_keys"] == 18)
        s.record_attempt(L, True, 44, False)
        check("best does not regress", s.lesson(L.slug)["best_keys"] == 18)
        check("clean run flagged", s.lesson(L.slug)["clean_run"])
        check("attempts counted", s.lesson(L.slug)["attempts"] == 3)


def test_streak():
    with tempfile.TemporaryDirectory() as tmp:
        s = State(Path(tmp) / "state.json")
        s.record_attempt(FakeLesson(), True, 15, False)
        check("first day starts a streak", s.streak_days() == 1)

        s.data["streak"]["last_day"] = (date.today() - timedelta(days=1)).isoformat()
        s.data["streak"]["days"] = 4
        s.touch_streak()
        check("consecutive day extends the streak", s.data["streak"]["days"] == 5)

        s.data["streak"]["last_day"] = (date.today() - timedelta(days=3)).isoformat()
        check("a gap breaks the streak", s.streak_days() == 0)

        s.touch_streak()
        check("streak restarts at 1", s.data["streak"]["days"] == 1)
        check("best is remembered", s.data["streak"]["best"] == 5)


def test_persistence():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "state.json"
        s = State(p)
        s.record_attempt(FakeLesson(), True, 15, False)
        s.save()
        again = State(p)
        check("state survives a round trip", again.lesson("99-01-test")["best_keys"] == 15)
        check("skills survive a round trip", "alpha" in again.data["skills"])

        p.write_text("{ not json at all")
        recovered = State(p)
        check("corrupt state recovers instead of crashing", recovered.data["lessons"] == {})
        check("corrupt state is kept for inspection", p.with_suffix(".json.corrupt").exists())


# ---------------------------------------------------------------- real content
def test_shipped_lessons():
    from engine import lesson as L
    lessons = L.load_all()
    check("lessons are on disk", len(lessons) > 0, "none found")
    ids = [l.id for l in lessons]
    check("ids are unique", len(ids) == len(set(ids)),
          f"{len(ids) - len(set(ids))} duplicates")

    import json
    cur = json.loads((ROOT / "curriculum.json").read_text())
    by_chapter = {ch["n"]: set(ch["skills"]) for b in cur["belts"] for ch in b["chapters"]}
    # A lesson may exercise its own chapter's skills or any taught earlier —
    # that is what makes a capstone or scenario possible. What it may not do
    # is use a skill from a chapter the player has not reached yet.
    stray = []
    for l in lessons:
        available = set()
        for n, skills in by_chapter.items():
            if n <= l.chapter:
                available |= skills
        for sk in l.skills:
            if sk not in available:
                stray.append(f"{l.id}:{sk}")
    check("no skills from unreached chapters", not stray, ", ".join(stray[:6]))

    thin = [l.id for l in lessons if l.type != "drill" and len(l.hints) < 2]
    check("every lesson has hints", not thin, ", ".join(thin[:6]))


def main():
    print("\n  engine tests\n")
    for fn in [
        test_parsing, test_validation, test_find_surfaces_broken_files,
        test_verify_decode,
        test_normalise, test_checking,
        test_decoy_files, test_isolation, test_arrow_detection, test_arrow_tax_is_real,
        test_grading_curve, test_srs,
        test_personal_bests, test_streak, test_persistence, test_shipped_lessons,
    ]:
        fn()
    print(f"\n  {len(PASSED)} passed, {len(FAILED)} failed\n")
    if FAILED:
        for f in FAILED:
            print(f"    FAILED: {f}")
        print()
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
