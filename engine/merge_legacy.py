"""Merge the staged legacy capstones into their chapters.

Run after a chapter's lessons are written, so the capstone takes the next
free number and nothing collides. Bumps that chapter's target in
curriculum.json so `./dojo map` does not report the chapter as short.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT / ".dojo" / "staging"
LESSONS = ROOT / "lessons"
CURRICULUM = ROOT / "curriculum.json"


def chapter_dir(n):
    for p in LESSONS.iterdir():
        if p.is_dir() and p.name.startswith(f"{n}-"):
            return p
    raise SystemExit(f"no directory for chapter {n}")


def next_number(d, chapter):
    used = []
    for p in d.glob("*.lesson"):
        m = re.match(rf"{chapter}-(\d+)-", p.name)
        if m:
            used.append(int(m.group(1)))
    return max(used, default=0) + 1


def merge(only=None, dry=False):
    if not STAGING.exists():
        raise SystemExit("nothing staged — run: python3 -m engine.convert_legacy")
    cur = json.loads(CURRICULUM.read_text())
    bumped = []
    for staged in sorted(STAGING.glob("*.lesson")):
        chapter, slug = staged.stem.split("--", 1)
        if only and chapter not in only:
            continue
        d = chapter_dir(chapter)
        num = next_number(d, chapter)
        new_id = f"{chapter}-{num:02d}"
        text = staged.read_text().replace(f"id: {chapter}-CAP", f"id: {new_id}", 1)
        target = d / f"{new_id}-{slug}.lesson"
        print(f"  {staged.name:<28} -> {target.relative_to(ROOT)}")
        if dry:
            continue
        target.write_text(text, encoding="utf-8")
        staged.unlink()
        for b in cur["belts"]:
            for ch in b["chapters"]:
                if ch["n"] == chapter and num > ch["target"]:
                    ch["target"] = num
                    bumped.append(f"{chapter}->{num}")
    if not dry:
        CURRICULUM.write_text(json.dumps(cur, indent=2) + "\n")
        if bumped:
            print(f"\n  targets bumped: {', '.join(bumped)}")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    sys.exit(merge(only=set(args) or None, dry="--dry" in sys.argv))
