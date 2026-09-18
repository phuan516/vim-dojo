"""vim-dojo command line."""
import json
import random
import sys
from datetime import date
from pathlib import Path

from engine import lesson as L
from engine import ui
from engine.runner import Attempt
from engine.state import State

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum.json"


def curriculum():
    return json.loads(CURRICULUM.read_text(encoding="utf-8"))


def chapter_index():
    """chapter number -> (belt dict, chapter dict)"""
    idx = {}
    for belt in curriculum()["belts"]:
        for ch in belt["chapters"]:
            idx[ch["n"]] = (belt, ch)
    return idx


# ---------------------------------------------------------------- selection
def ordered_lessons():
    return L.load_all()


def next_lesson(state):
    """The first lesson not yet cleared, honouring an explicit `goto`."""
    lessons = ordered_lessons()
    if not lessons:
        return None
    pinned = state.data.get("current")
    if pinned:
        for l in lessons:
            if l.slug == pinned and not state.is_cleared(l.slug):
                return l
    for l in lessons:
        if not state.is_cleared(l.slug):
            return l
    return None


def review_queue(state, limit=8):
    """Cleared lessons whose skills have fallen due, weakest first."""
    due = set(state.due_skills())
    if not due:
        return []
    candidates = []
    for l in ordered_lessons():
        if not state.is_cleared(l.slug):
            continue
        overlap = due.intersection(l.skills)
        if overlap:
            weakness = min(state.mastery(s) for s in overlap)
            candidates.append((weakness, -len(overlap), l))
    candidates.sort(key=lambda c: (c[0], c[1]))
    return [c[2] for c in candidates[:limit]]


# ---------------------------------------------------------------- rendering
def show_header(l, state):
    idx = chapter_index()
    belt, ch = idx.get(l.chapter, ({"belt": "—"}, {"title": "—"}))
    rec = state.lesson(l.slug)
    ui.title(f"{l.id}  {l.title}")
    print(f"  {ui.D}{ch['title']}   {ui.belt_tag(belt['belt'])}{ui.R}")
    bits = [f"{ui.D}par{ui.R} {l.par} keys", f"{ui.D}~{l.minutes} min{ui.R}"]
    if l.vscode:
        bits.append(f"{ui.D}in VS Code:{ui.R} {l.vscode}")
    if rec["best_keys"]:
        bits.append(f"{ui.D}your best{ui.R} {rec['best_keys']}")
    print("  " + "   ".join(bits))
    ui.rule()


def cmd_brief(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    show_header(l, state)
    ui.indent(l.brief)
    print()
    return 0


def cmd_keys(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    ui.title("keys for this lesson")
    ui.rule()
    ui.indent(l.keys or "(nothing new — this one is practice)")
    print()
    return 0


def cmd_hint(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    n = state.hints_used(l.slug)
    if n >= len(l.hints):
        print(f"\n  {ui.D}No hints left. Try ./dojo solution{ui.R}\n")
        return 0
    n = state.use_hint(l.slug)
    state.save()
    print(f"\n  {ui.YEL}{ui.B}hint {n} of {len(l.hints)}{ui.R}")
    ui.indent(l.hints[n - 1])
    print()
    return 0


def cmd_solution(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    ui.title(f"solution — {l.id} {l.title}")
    ui.rule()
    ui.indent(l.solution or "(no written solution for this one)")
    print()
    return 0


# ---------------------------------------------------------------- playing
def resolve(args, state):
    ident = args[0] if args else None
    try:
        l = L.find(ident) if ident else next_lesson(state)
    except L.LessonError as e:
        print(f"\n  {ui.YEL}{e}{ui.R}\n")
        return None
    if not l:
        if ident:
            print(f"\n  {ui.YEL}No lesson matches '{ident}'. Try ./dojo map{ui.R}\n")
        else:
            print(f"\n  {ui.GRN}{ui.B}Every lesson cleared.{ui.R} "
                  f"{ui.D}./dojo review keeps it sharp.{ui.R}\n")
        return None
    return l


def play(l, state, replay=False):
    att = Attempt(l)
    att.prepare(force=replay)
    if replay:
        state.reset_hints(l.slug)

    show_header(l, state)
    ui.indent(l.brief)
    print()
    ui.rule()
    print(f"  {ui.D}files:{ui.R} {', '.join(l.open_files)}   "
          f"{ui.D}{att.dir.relative_to(ROOT)}{ui.R}")
    print(f"  {ui.D}Enter to open vim   ·   Ctrl-C to just read   ·   "
          f"inside vim, :wq to finish{ui.R} ", end="")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        print("\n")
        return 0

    if l.type == "drill":
        return run_drill(l, att, state)

    att.launch()
    print()
    return grade(l, att, state)


def grade(l, att, state):
    ui.rule()
    passed, failures = att.check()
    keys = att.keystrokes()
    arrows = att.used_arrows()
    ui.rule()

    if not passed:
        print(f"\n  {ui.RED}{ui.B}Not yet.{ui.R} Fix the differences above, then "
              f"{ui.B}./dojo check{ui.R}")
        print(f"  {ui.D}stuck? ./dojo hint   ·   start over? ./dojo reset{ui.R}\n")
        state.record_attempt(l, False, keys, arrows, att.seconds)
        state.save()
        return 1

    g = state.record_attempt(l, True, keys, arrows, att.seconds)
    print(f"\n  {ui.GRN}{ui.B}✔ {l.id} CLEARED{ui.R}\n")
    if keys:
        verdict = (f"{ui.GRN}under par ⭐{ui.R}" if keys <= l.par
                   else f"{ui.YEL}over par — ./dojo replay{ui.R}" if keys <= l.par * 2
                   else f"{ui.RED}way over — read ./dojo solution, then ./dojo replay{ui.R}")
        print(f"  keystrokes {ui.B}{keys}{ui.R}   par {l.par}   {verdict}")
        if att.seconds:
            print(f"  {ui.D}time {att.seconds}s{ui.R}")
        print(f"  {ui.GRN}🏅 no arrow keys, no mouse{ui.R}" if not arrows
              else f"  {ui.D}(arrow keys or mouse detected — hjkl is faster than you think){ui.R}")

    for skill in l.skills:
        s = state.data["skills"][skill]
        print(f"  {ui.D}{skill:<22}{ui.R} {ui.bar(s['mastery'], 1.0, 14)} "
              f"{ui.D}next review in {s['interval']}d{ui.R}")

    state.data["current"] = None
    state.save()

    nxt = next_lesson(state)
    if nxt:
        print(f"\n  next: {ui.B}{nxt.id} {nxt.title}{ui.R}  {ui.D}(./dojo play){ui.R}\n")
    else:
        print(f"\n  {ui.B}{ui.MAG}That was the last one. You can drive vim.{ui.R}\n")
    return 0


def run_drill(l, att, state):
    """Same small edit, many times, timed. Finger memory, not understanding."""
    reps = l.reps
    times = []
    for i in range(1, reps + 1):
        att.prepare(force=True)
        print(f"\n  {ui.B}rep {i}/{reps}{ui.R}  {ui.D}go{ui.R}")
        att.launch()
        passed, _ = att.check(verbose=False)
        mark = f"{ui.GRN}✔{ui.R}" if passed else f"{ui.RED}✘{ui.R}"
        print(f"  {mark}  {att.seconds}s   {att.keystrokes()} keys")
        if passed:
            times.append(att.seconds)
        state.record_attempt(l, passed, att.keystrokes(), att.used_arrows(), att.seconds)
    state.save()
    ui.rule()
    if times:
        print(f"\n  {ui.B}{len(times)}/{reps} clean{ui.R}   "
              f"best {ui.GRN}{min(times)}s{ui.R}   "
              f"last {times[-1]}s   median {sorted(times)[len(times)//2]}s\n")
    else:
        print(f"\n  {ui.YEL}No clean reps. Read ./dojo solution and drill again.{ui.R}\n")
    return 0


def cmd_play(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    state.data["current"] = l.slug
    state.save()
    return play(l, state)


def cmd_replay(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    return play(l, state, replay=True)


def cmd_check(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    att = Attempt(l)
    if not att.dir.exists():
        print(f"\n  {ui.YEL}Nothing to check yet — run ./dojo play{ui.R}\n")
        return 1
    return grade(l, att, state)


def cmd_reset(args, state):
    l = resolve(args, state)
    if not l:
        return 1
    Attempt(l).wipe()
    state.reset_hints(l.slug)
    state.save()
    print(f"\n  {ui.D}{l.id} reset{ui.R}\n")
    return 0


def cmd_goto(args, state):
    if not args:
        print("\n  usage: ./dojo goto 10-03   (or a chapter: ./dojo goto 10)\n")
        return 1
    try:
        l = L.find(args[0])
    except L.LessonError as e:
        print(f"\n  {ui.YEL}{e}{ui.R}\n")
        return 1
    if not l:
        matches = L.load_all(chapter=args[0].zfill(2))
        if matches:
            l = matches[0]
    if not l:
        print(f"\n  {ui.YEL}No lesson '{args[0]}'. Try ./dojo map{ui.R}\n")
        return 1
    state.data["current"] = l.slug
    state.save()
    print(f"\n  now on {ui.B}{l.id} {l.title}{ui.R}  {ui.D}(./dojo play){ui.R}\n")
    return 0


# ---------------------------------------------------------------- review & drill
def cmd_review(args, state):
    queue = review_queue(state, limit=int(args[0]) if args and args[0].isdigit() else 8)
    if not queue:
        due = state.due_skills()
        ui.banner()
        if due:
            print(f"  {ui.D}Skills are due ({', '.join(due[:6])}) but the lessons that "
                  f"teach them aren't cleared yet.{ui.R}")
            print(f"  {ui.D}Carry on with ./dojo play{ui.R}\n")
        else:
            print(f"  {ui.GRN}Nothing due for review. Your memory is ahead of schedule.{ui.R}")
            print(f"  {ui.D}./dojo play for new ground, ./dojo drill for speed{ui.R}\n")
        return 0
    ui.banner()
    print(f"  {ui.B}Review — {len(queue)} lessons whose skills have gone stale{ui.R}\n")
    for l in queue:
        print(f"    {ui.D}{l.id}{ui.R}  {l.title}")
    print(f"\n  {ui.D}Enter to start, Ctrl-C to bail{ui.R} ", end="")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        print("\n")
        return 0
    for l in queue:
        play(l, state, replay=True)
    return 0


def cmd_drill(args, state):
    """Drill a named skill, the weakest skill, or a specific drill lesson."""
    drills = [l for l in ordered_lessons() if l.type == "drill"]
    if not drills:
        print(f"\n  {ui.YEL}No drills authored yet.{ui.R}\n")
        return 1
    if args:
        want = args[0].lower()
        pool = [d for d in drills if want in d.slug.lower()
                or any(want in s.lower() for s in d.skills)]
        if not pool:
            print(f"\n  {ui.YEL}No drill for '{args[0]}'. "
                  f"Skills with drills: {', '.join(sorted({s for d in drills for s in d.skills}))[:300]}{ui.R}\n")
            return 1
    else:
        weak = state.weakest_skills(6)
        pool = [d for d in drills if any(s in weak for s in d.skills)] or drills
    d = random.choice(pool)
    return play(d, state, replay=True)


def cmd_scenario(args, state):
    pool = [l for l in ordered_lessons() if l.type in ("scenario", "boss")]
    if not pool:
        print(f"\n  {ui.YEL}No scenarios authored yet.{ui.R}\n")
        return 1
    if args:
        pool = [l for l in pool if args[0].lower() in l.slug.lower()] or pool
    unseen = [l for l in pool if not state.is_cleared(l.slug)]
    return play((unseen or pool)[0], state)


# ---------------------------------------------------------------- overview
def cmd_map(args, state):
    cur = curriculum()
    lessons = ordered_lessons()
    by_chapter = {}
    for l in lessons:
        by_chapter.setdefault(l.chapter, []).append(l)
    only = args[0].zfill(2) if args else None

    ui.banner()
    for belt in cur["belts"]:
        if only and not any(c["n"] == only for c in belt["chapters"]):
            continue
        print(f"  {ui.belt_tag(belt['belt'])} {ui.B}{belt['name']}{ui.R}")
        print(f"     {ui.D}{belt['premise']}{ui.R}")
        for ch in belt["chapters"]:
            if only and ch["n"] != only:
                continue
            got = by_chapter.get(ch["n"], [])
            done = sum(1 for l in got if state.is_cleared(l.slug))
            target = ch["target"]
            written = len(got)
            status = (f"{ui.D}not written yet{ui.R}" if not written
                      else f"{done}/{written} done")
            short = f"{ui.D}({written}/{target} written){ui.R}" if written < target else ""
            print(f"     {ch['n']}  {ch['title']:<36} {ui.bar(done, max(written,1), 12)} "
                  f"{status} {short}")
            if only:
                for l in got:
                    mark = (f"{ui.GRN}✔{ui.R}" if state.is_cleared(l.slug) else f"{ui.D}·{ui.R}")
                    tag = "" if l.type == "lesson" else f" {ui.D}[{l.type}]{ui.R}"
                    print(f"          {mark} {l.id}  {l.title}{tag}")
        print()
    if not only:
        print(f"  {ui.D}./dojo map 10   to see one chapter's lessons{ui.R}\n")
    return 0


def cmd_stats(args, state):
    lessons = ordered_lessons()
    cleared = [l for l in lessons if state.is_cleared(l.slug)]
    hist = state.data["history"]
    days = sorted({h["day"] for h in hist})
    clean = sum(1 for l in lessons if state.lesson(l.slug)["clean_run"])

    ui.banner()
    print(f"  {ui.B}Progress{ui.R}")
    ui.kv("lessons", f"{len(cleared)}/{len(lessons)} cleared "
                     f"{ui.bar(len(cleared), max(len(lessons),1), 20)}")
    ui.kv("under par", f"{clean} lessons beaten cleanly (no arrows, under par)")
    ui.kv("attempts", str(len(hist)))
    ui.kv("days trained", str(len(days)))
    ui.kv("streak", f"{state.streak_days()} days (best {state.data['streak']['best']})")
    ui.kv("started", state.data["created"])

    skills = state.data["skills"]
    if skills:
        strong = sorted(skills.items(), key=lambda kv: -kv[1]["mastery"])[:5]
        weak = sorted((kv for kv in skills.items() if kv[1]["reps"] or kv[1]["lapses"]),
                      key=lambda kv: kv[1]["mastery"])[:5]
        print(f"\n  {ui.B}Strongest{ui.R}")
        for name, s in strong:
            print(f"    {name:<24} {ui.bar(s['mastery'], 1.0, 16)}")
        print(f"\n  {ui.B}Shakiest{ui.R}")
        for name, s in weak:
            n = s["lapses"]
            tail = "clean so far" if not n else f"{n} lapse" + ("" if n == 1 else "s")
            print(f"    {name:<24} {ui.bar(s['mastery'], 1.0, 16, ui.YEL)} "
                  f"{ui.D}{tail}{ui.R}")
        due = state.due_skills()
        print(f"\n  {ui.D}{len(due)} skills due for review today{ui.R}")
    if hist:
        recent = [h for h in hist if h.get("keys")][-40:]
        if recent:
            avg = sum(h["keys"] for h in recent) / len(recent)
            arrow_rate = sum(1 for h in recent if h["arrows"]) / len(recent)
            print(f"  {ui.D}last 40 attempts: {avg:.0f} keys average, "
                  f"{arrow_rate*100:.0f}% used arrows or mouse{ui.R}")
    print()
    return 0


def cmd_skills(args, state):
    skills = state.data["skills"]
    if not skills:
        print(f"\n  {ui.D}No skills tracked yet — play a lesson.{ui.R}\n")
        return 0
    ui.banner()
    print(f"  {ui.B}Skill{ui.R}{'':<20}{ui.D}mastery              due       reps{ui.R}")
    for name, s in sorted(skills.items(), key=lambda kv: (-kv[1]["mastery"], kv[0])):
        overdue = s["due"] <= date.today().isoformat() and s["reps"] > 0
        due = f"{ui.YEL}due now{ui.R}" if overdue else f"{ui.D}{s['due']}{ui.R}"
        print(f"  {name:<25}{ui.bar(s['mastery'],1.0,16)}  {due:<20} {ui.D}{s['reps']}{ui.R}")
    print()
    return 0


def cmd_today(args, state):
    """What to actually do right now."""
    cur = curriculum()["pace"]
    done = state.count_today()
    queue = review_queue(state, limit=cur["review_per_day"])
    nxt = next_lesson(state)
    weak = state.weakest_skills(3)

    ui.banner()
    streak = state.streak_days()
    flame = f"{ui.YEL}🔥 {streak} day streak{ui.R}" if streak else f"{ui.D}streak broken — start again today{ui.R}"
    print(f"  {flame}   {ui.D}{done} sets done today{ui.R}\n")
    print(f"  {ui.B}Today's plan{ui.R}")
    n = 1
    if queue:
        print(f"    {n}. {ui.B}./dojo review{ui.R}   {ui.D}{len(queue)} lessons have gone stale{ui.R}")
        n += 1
    if nxt:
        print(f"    {n}. {ui.B}./dojo play{ui.R}     {ui.D}{nxt.id} {nxt.title}{ui.R}")
        n += 1
    if weak:
        print(f"    {n}. {ui.B}./dojo drill{ui.R}    {ui.D}weakest: {', '.join(weak)}{ui.R}")
    print(f"\n  {ui.D}Two lessons a day finishes the dojo in a year. "
          f"Four a day and you will forget half of it.{ui.R}\n")
    return 0


def cmd_doctor(args, state):
    """Validate every lesson file — used by content authors and CI."""
    problems = []
    seen_ids = {}
    count = 0
    for p in L.lesson_paths():
        try:
            l = L.Lesson(p)
        except L.LessonError as e:
            problems.append(str(e))
            continue
        count += 1
        if l.id in seen_ids:
            problems.append(f"{p}: duplicate id {l.id} (also {seen_ids[l.id]})")
        seen_ids[l.id] = p.name
        for f in l.open_files:
            if f not in l.start and f not in l.expected:
                problems.append(f"{p}: opens '{f}' which is in neither @start nor @expected")
        for name in l.expected:
            if name in l.start and l.start[name] == l.expected[name]:
                problems.append(f"{p}: '{name}' expected is identical to start — nothing to do")
        if l.type != "drill" and len(l.hints) < 2:
            problems.append(f"{p}: only {len(l.hints)} hints (want at least 2)")
        if not l.solution.strip():
            problems.append(f"{p}: no @solution")

    idx = chapter_index()
    for p in L.lesson_paths():
        ch = p.parent.name.split("-")[0]
        if ch not in idx:
            problems.append(f"{p}: chapter {ch} is not in curriculum.json")

    print()
    if problems:
        print(f"  {ui.RED}{len(problems)} problems in {count} lessons{ui.R}\n")
        for pr in problems[:60]:
            print(f"    {pr}")
        if len(problems) > 60:
            print(f"    {ui.D}… and {len(problems)-60} more{ui.R}")
        print()
        return 1
    print(f"  {ui.GRN}{count} lessons, all valid{ui.R}\n")
    return 0


def cmd_verify(args, state):
    from engine import verify
    return verify.run(args)


def cmd_cheat(args, state):
    import subprocess
    subprocess.call([os.environ.get("PAGER", "less"), str(ROOT / "CHEATSHEET.md")])
    return 0


def cmd_help(args, state):
    print(f"""
  {ui.B}vim-dojo{ui.R}

    {ui.B}./dojo{ui.R}              what to do today
    {ui.B}./dojo play{ui.R} [id]    next lesson, or one by id
    {ui.B}./dojo check{ui.R}        grade what's in the work folder
    {ui.B}./dojo review{ui.R}       spaced repetition — whatever has gone stale
    {ui.B}./dojo drill{ui.R} [skill] same edit ten times, against the clock
    {ui.B}./dojo scenario{ui.R}     a real multi-file job on the sample codebase

    {ui.B}./dojo hint{ui.R}         one nudge at a time
    {ui.B}./dojo keys{ui.R}         the keys this lesson is about
    {ui.B}./dojo solution{ui.R}     the answer, and why it is the fast way
    {ui.B}./dojo brief{ui.R}        re-read the mission

    {ui.B}./dojo map{ui.R} [ch]     the whole curriculum, or one chapter
    {ui.B}./dojo stats{ui.R}        progress, streak, strongest and shakiest
    {ui.B}./dojo skills{ui.R}       every tracked skill and when it's next due
    {ui.B}./dojo goto{ui.R} 10-03   jump to a lesson or chapter
    {ui.B}./dojo replay{ui.R}       wipe this lesson and do it again, faster
    {ui.B}./dojo reset{ui.R}        throw away this attempt
    {ui.B}./dojo cheat{ui.R}        the VS Code -> vim cheatsheet
    {ui.B}./dojo doctor{ui.R}       validate all lesson files
    {ui.B}./dojo verify{ui.R} id keys  solve a lesson non-interactively (authors)
""")
    return 0


import os  # noqa: E402  (used by cmd_cheat)

COMMANDS = {
    "": cmd_today, "today": cmd_today, "status": cmd_today,
    "play": cmd_play, "start": cmd_play,
    "check": cmd_check, "hint": cmd_hint, "keys": cmd_keys,
    "solution": cmd_solution, "solve": cmd_solution, "brief": cmd_brief,
    "review": cmd_review, "drill": cmd_drill, "scenario": cmd_scenario,
    "map": cmd_map, "stats": cmd_stats, "skills": cmd_skills,
    "goto": cmd_goto, "replay": cmd_replay, "reset": cmd_reset,
    "cheat": cmd_cheat, "doctor": cmd_doctor, "verify": cmd_verify,
    "help": cmd_help, "-h": cmd_help, "--help": cmd_help,
}


def main(argv):
    cmd = argv[0] if argv else ""
    args = argv[1:]
    fn = COMMANDS.get(cmd)
    if not fn:
        print(f"\n  {ui.YEL}no command '{cmd}'{ui.R}")
        return cmd_help([], None)
    state = State()
    try:
        rc = fn(args, state)
    except KeyboardInterrupt:
        print("\n")
        return 130
    state.save()
    return rc or 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
