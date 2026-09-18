"""Lesson file format: parsing and discovery.

A lesson is one plain-text file, `lessons/<chapter>/<id>-<slug>.lesson`.
Sections begin with `@name` at column 0. Everything after a section header
belongs to it until the next header. Example:

    @meta
    title: Change inside quotes
    skills: ci-quote, text-objects
    par: 24

    @brief
    The mission, in prose.

    @keys
    | `ci"` | change inside the quotes |

    @hints
    First nudge.
    --
    Second, more explicit nudge.

    @solution
    The full answer and why it is the fast way.

    @start config.ts
    ...file contents as the player finds them...

    @expected config.ts
    ...file contents as they must end up...

`@start` and `@expected` may appear many times for multi-file lessons.
A file present in `@expected` but not `@start` must be created by the player.
A file in `@start` with no `@expected` twin must be left untouched.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"

# Only these seven words start a section. Anything else at column 0 after an
# @ is content -- `@a` plays macro a, `@injectable()` decorates a class, and
# neither is a section header. A line that really does begin with one of these
# words is escaped as `\@meta`.
SECTION_NAMES = ("meta", "brief", "keys", "hints", "solution", "start", "expected")
SECTION = re.compile(r"^@(" + "|".join(SECTION_NAMES) + r")(?:\s+(.*))?$")
VALID_TYPES = {"lesson", "drill", "scenario", "boss"}


class LessonError(Exception):
    pass


class Lesson:
    def __init__(self, path):
        self.path = Path(path)
        self.meta = {}
        self.brief = ""
        self.keys = ""
        self.hints = []
        self.solution = ""
        self.start = {}
        self.expected = {}
        self._parse()

    # ---------- parsing ----------
    def _parse(self):
        raw = self.path.read_text(encoding="utf-8")
        sections = []
        current = None
        for line in raw.split("\n"):
            m = SECTION.match(line)
            if m:
                current = (m.group(1), (m.group(2) or "").strip(), [])
                sections.append(current)
            elif current is not None:
                # A file line that genuinely starts with @ (a bare TypeScript
                # decorator, say) is written as \@ so it is not read as a section.
                current[2].append(line[1:] if line.startswith("\\@") else line)

        if not sections:
            raise LessonError(f"{self.path}: no @sections found")

        for name, arg, body in sections:
            text = "\n".join(body).strip("\n")
            if name == "meta":
                self._parse_meta(text)
            elif name == "brief":
                self.brief = text
            elif name == "keys":
                self.keys = text
            elif name == "hints":
                self.hints = [h.strip("\n") for h in text.split("\n--\n") if h.strip()]
            elif name == "solution":
                self.solution = text
            elif name == "start":
                if not arg:
                    raise LessonError(f"{self.path}: @start needs a filename")
                self.start[arg] = text + "\n"
            elif name == "expected":
                if not arg:
                    raise LessonError(f"{self.path}: @expected needs a filename")
                self.expected[arg] = text + "\n"


        self._validate()

    def _parse_meta(self, text):
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                raise LessonError(f"{self.path}: bad meta line {line!r}")
            k, v = line.split(":", 1)
            self.meta[k.strip()] = v.strip()

    def _validate(self):
        for required in ("title", "skills", "par"):
            if required not in self.meta:
                raise LessonError(f"{self.path}: meta is missing '{required}'")
        if self.type not in VALID_TYPES:
            raise LessonError(f"{self.path}: type '{self.type}' not in {VALID_TYPES}")
        if not self.brief.strip():
            raise LessonError(f"{self.path}: empty @brief")
        if not self.expected:
            raise LessonError(f"{self.path}: no @expected file — nothing to grade")
        try:
            int(self.meta["par"])
        except ValueError:
            raise LessonError(f"{self.path}: par must be a number")

    # ---------- derived ----------
    @property
    def id(self):
        return self.meta.get("id") or self.path.stem.split("-")[0]

    @property
    def slug(self):
        return self.path.stem

    @property
    def chapter(self):
        return self.meta.get("chapter") or self.path.parent.name.split("-")[0]

    @property
    def title(self):
        return self.meta["title"]

    @property
    def type(self):
        return self.meta.get("type", "lesson")

    @property
    def skills(self):
        return [s.strip() for s in self.meta["skills"].split(",") if s.strip()]

    @property
    def par(self):
        return int(self.meta["par"])

    @property
    def reps(self):
        return int(self.meta.get("reps", 1))

    @property
    def minutes(self):
        return int(self.meta.get("minutes", 4))

    @property
    def vscode(self):
        return self.meta.get("vscode", "")

    @property
    def open_files(self):
        """Which files vim opens with, in order."""
        declared = self.meta.get("open")
        if declared:
            return [f.strip() for f in declared.split() if f.strip()]
        return list(self.start.keys()) or list(self.expected.keys())

    def __repr__(self):
        return f"<Lesson {self.slug}>"


# ---------- discovery ----------
def chapter_dirs():
    if not LESSONS.exists():
        return []
    return sorted(d for d in LESSONS.iterdir() if d.is_dir() and not d.name.startswith("."))


def lesson_paths(chapter=None):
    out = []
    for d in chapter_dirs():
        if chapter and not d.name.startswith(str(chapter).zfill(2)):
            continue
        out.extend(sorted(d.glob("*.lesson")))
    return out


def load_all(chapter=None, quiet=True):
    """Every parseable lesson, in curriculum order. Broken files are reported once."""
    lessons, broken = [], []
    for p in lesson_paths(chapter):
        try:
            lessons.append(Lesson(p))
        except LessonError as e:
            broken.append(str(e))
    if broken and not quiet:
        for b in broken:
            print(f"  ! {b}")
    return lessons


def find(ident):
    """Look a lesson up by id, slug, or a unique fragment of either."""
    if ident is None:
        return None
    ident = str(ident).strip().lower()
    all_lessons = load_all()
    for l in all_lessons:
        if l.id.lower() == ident or l.slug.lower() == ident:
            return l
    hits = [l for l in all_lessons if ident in l.slug.lower() or ident in l.title.lower()]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        raise LessonError(
            f"'{ident}' matches {len(hits)} lessons: " + ", ".join(h.slug for h in hits[:6])
        )
    # Nothing parsed under that name. If a file exists for it, the file is
    # broken, and silence here would send the author hunting in the wrong place.
    for path in lesson_paths():
        if path.stem.lower().startswith(ident):
            Lesson(path)  # raises LessonError with the real reason
    return None
