"""One-off: convert the original 14 levels into the .lesson format.

They were good exercises and they become the capstone of the chapter that
teaches their skill. Run once into a staging directory, then merge when the
chapter authors have finished numbering their lessons.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "levels"
STAGING = ROOT / ".dojo" / "staging"

# old level -> (new chapter, type, skills)
MAP = {
    # Each old level lands in the chapter that has taught every key it needs.
    # The original ordering assumed you learn delete on day one; this
    # curriculum does not, so several move a long way down.
    "01": ("08", "scenario", "delete-d, change-c, yank-y, put-p, undo, insert-i"),
    "02": ("07", "scenario", "goto-line, paragraph-motion, scroll-half, word-w, line-start"),
    "03": ("09", "scenario", "op-motion, delete-d, change-c, yank-y, put-p, replace-r"),
    "04": ("11", "scenario", "dot-repeat, dot-design, cgn, obj-word, obj-quote, obj-paren"),
    "05": ("10", "scenario", "obj-quote, inner-vs-around, find-f, find-t, op-motion"),
    "06": ("14", "scenario", "search-slash, search-star, search-motion, sub-basic"),
    "07": ("14", "scenario", "sub-basic, sub-range, sub-confirm, sub-case"),
    "08": ("22", "scenario", "visual-char, visual-line, visual-block, block-insert"),
    "09": ("17", "scenario", "jump-back, jumplist, marks-set, marks-jump, match-percent"),
    "10": ("16", "scenario", "buffer-switch, buffer-list, split-window, window-nav"),
    "11": ("18", "scenario", "edit-file, find-path, netrw, buffer-switch"),
    "12": ("19", "scenario", "vimgrep, quickfix-nav, cdo"),
    "13": ("21", "scenario", "macro-record, macro-play, macro-count"),
    "14": ("32", "boss", "multi-file-refactor, feature-implementation, speed-under-pressure"),
}

CHAPTER_DIR = {p.name.split("-")[0]: p.name for p in (ROOT / "lessons").iterdir() if p.is_dir()}


def meta_of(d, key):
    m = re.search(rf"^{key}=(.*)$", (d / "meta").read_text(), re.M)
    return m.group(1).strip() if m else ""


def read(p):
    return p.read_text(encoding="utf-8").rstrip("\n") if p.exists() else ""


def dedent_brief(text):
    """Old briefs were indented two spaces for direct printing."""
    lines = text.split("\n")
    if all(not l.strip() or l.startswith("  ") for l in lines):
        lines = [l[2:] if l.startswith("  ") else l for l in lines]
    return "\n".join(lines).strip("\n")


def files_of(d, sub):
    base = d / sub
    if not base.exists():
        return {}
    out = {}
    for p in sorted(base.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(base))] = p.read_text(encoding="utf-8", errors="replace").rstrip("\n")
    return out


def convert(old):
    d = LEGACY / CHAPTER_DIR_LEGACY[old]
    chapter, ltype, skills = MAP[old]
    title = meta_of(d, "title")
    # strip the old "Belt:" style prefixes, keep it a sentence
    title = re.sub(r"^(Survival|Boss):\s*", "", title)
    title = f"Capstone — {title[0].lower() + title[1:]}" if ltype == "scenario" else f"Boss — {title[0].lower() + title[1:]}"

    hints = [h.strip("\n") for h in read(d / "hints.md").split("\n---\n") if h.strip()]
    hints = [dedent_brief(h) for h in hints]
    start = files_of(d, "start")
    expected = files_of(d, "expected")

    parts = [
        "@meta",
        f"id: {chapter}-CAP",
        f"title: {title[:46]}",
        f"chapter: {chapter}",
        f"type: {ltype}",
        f"skills: {skills}",
        f"par: {meta_of(d, 'par')}",
        f"minutes: {max(6, int(meta_of(d, 'par') or 100) // 25)}",
        f"vscode: {meta_of(d, 'vscode')}",
        f"open: {meta_of(d, 'open')}",
        "",
        "@brief",
        dedent_brief(read(d / "brief.md")),
        "",
        "@keys",
        dedent_brief(read(d / "keys.md")),
        "",
        "@hints",
        "\n--\n".join(hints),
        "",
        "@solution",
        dedent_brief(read(d / "solution.md")),
        "",
    ]
    for name, content in start.items():
        parts += [f"@start {name}", content, ""]
    for name, content in expected.items():
        parts += [f"@expected {name}", content, ""]

    return chapter, "\n".join(parts)


CHAPTER_DIR_LEGACY = {p.name.split("-")[0]: p.name for p in LEGACY.iterdir() if p.is_dir()}


def main():
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    for old in sorted(MAP):
        chapter, text = convert(old)
        slug = CHAPTER_DIR_LEGACY[old].split("-", 1)[1]
        out = STAGING / f"{chapter}--{slug}.lesson"
        out.write_text(text, encoding="utf-8")
        print(f"  level {old} -> chapter {chapter}  {out.name}")
    print(f"\n  {len(MAP)} legacy levels staged in {STAGING.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
