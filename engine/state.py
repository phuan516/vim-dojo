"""Player state: progress, spaced repetition, streaks, personal bests.

Everything lives in one JSON file so it stays inspectable and easy to back up.
The spaced-repetition scheduler is SM-2 with the grading adapted to editing:
you are graded not on whether you remembered a fact but on whether your fingers
produced the edit, quickly, without reaching for the arrow keys.
"""
import json
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / ".dojo" / "state.json"

DEFAULT = {
    "version": 2,
    "created": None,
    "current": None,
    "streak": {"days": 0, "best": 0, "last_day": None},
    "skills": {},
    "lessons": {},
    "history": [],
    "hints_used": {},
}

# SM-2 tuned for motor skills: first repeat same day, then 2 days, then ease-scaled.
FIRST_INTERVALS = [0, 2]
MIN_EASE = 1.3


def today():
    return date.today().isoformat()


def now():
    return datetime.now().isoformat(timespec="seconds")


class State:
    def __init__(self, path=STATE_PATH):
        self.path = Path(path)
        self.data = json.loads(json.dumps(DEFAULT))
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                self.data.update(loaded)
            except json.JSONDecodeError:
                backup = self.path.with_suffix(".json.corrupt")
                self.path.rename(backup)
                print(f"  ! state was unreadable, moved to {backup.name}, starting fresh")
        if not self.data.get("created"):
            self.data["created"] = today()
        self._migrate()

    def _migrate(self):
        for key, default in DEFAULT.items():
            self.data.setdefault(key, json.loads(json.dumps(default)))

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self.data, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(self.path)

    # ---------- lessons ----------
    def lesson(self, slug):
        return self.data["lessons"].setdefault(
            slug,
            {"attempts": 0, "cleared": False, "best_keys": None, "first_cleared": None,
             "last_seen": None, "clean_run": False},
        )

    def is_cleared(self, slug):
        return self.data["lessons"].get(slug, {}).get("cleared", False)

    def record_attempt(self, lesson, passed, keys, used_arrows, seconds=None):
        rec = self.lesson(lesson.slug)
        rec["attempts"] += 1
        rec["last_seen"] = now()
        if passed:
            if not rec["cleared"]:
                rec["cleared"] = True
                rec["first_cleared"] = today()
            if keys and (rec["best_keys"] is None or keys < rec["best_keys"]):
                rec["best_keys"] = keys
            if not used_arrows and keys and keys <= lesson.par:
                rec["clean_run"] = True

        grade = self.grade(lesson, passed, keys, used_arrows)
        for skill in lesson.skills:
            self.review_skill(skill, grade)

        self.data["history"].append(
            {"day": today(), "at": now(), "lesson": lesson.slug, "passed": passed,
             "keys": keys, "arrows": used_arrows, "seconds": seconds, "grade": grade}
        )
        self.data["history"] = self.data["history"][-4000:]
        self.touch_streak()
        return grade

    @staticmethod
    def grade(lesson, passed, keys, used_arrows):
        """0-5, SM-2 style. Correctness first, then economy, then purity."""
        if not passed:
            return 1
        if not keys:
            return 3
        ratio = keys / max(lesson.par, 1)
        if ratio <= 1.0:
            g = 5
        elif ratio <= 1.5:
            g = 4
        elif ratio <= 2.5:
            g = 3
        else:
            g = 2
        if used_arrows and g > 2:
            g -= 1
        return g

    # ---------- spaced repetition ----------
    def skill(self, name):
        return self.data["skills"].setdefault(
            name,
            {"reps": 0, "ease": 2.5, "interval": 0, "due": today(), "lapses": 0,
             "mastery": 0.0, "last_grade": None},
        )

    def review_skill(self, name, grade):
        s = self.skill(name)
        s["last_grade"] = grade
        if grade < 3:
            s["reps"] = 0
            s["interval"] = 0
            s["lapses"] += 1
            s["mastery"] = max(0.0, s["mastery"] - 0.25)
            s["due"] = today()
        else:
            if s["reps"] < len(FIRST_INTERVALS):
                s["interval"] = FIRST_INTERVALS[s["reps"]] or 1
            else:
                s["interval"] = max(1, round(s["interval"] * s["ease"]))
            s["reps"] += 1
            s["mastery"] = min(1.0, s["mastery"] + (0.34 if grade == 5 else 0.2))
            s["due"] = (date.today() + timedelta(days=s["interval"])).isoformat()
        s["ease"] = max(
            MIN_EASE, s["ease"] + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
        )

    def due_skills(self):
        t = today()
        return sorted(
            (n for n, s in self.data["skills"].items() if s["due"] <= t and s["reps"] > 0),
            key=lambda n: (self.data["skills"][n]["mastery"], self.data["skills"][n]["due"]),
        )

    def weakest_skills(self, n=5):
        seen = [(k, v) for k, v in self.data["skills"].items() if v["reps"] > 0 or v["lapses"]]
        return [k for k, _ in sorted(seen, key=lambda kv: (kv[1]["mastery"], -kv[1]["lapses"]))[:n]]

    def mastery(self, name):
        return self.data["skills"].get(name, {}).get("mastery", 0.0)

    # ---------- streak ----------
    def touch_streak(self):
        st = self.data["streak"]
        t = date.today()
        last = st.get("last_day")
        if last == t.isoformat():
            return
        if last and date.fromisoformat(last) == t - timedelta(days=1):
            st["days"] += 1
        else:
            st["days"] = 1
        st["last_day"] = t.isoformat()
        st["best"] = max(st["best"], st["days"])

    def streak_days(self):
        st = self.data["streak"]
        last = st.get("last_day")
        if not last:
            return 0
        gap = (date.today() - date.fromisoformat(last)).days
        return st["days"] if gap <= 1 else 0

    def practised_today(self):
        return any(h["day"] == today() for h in self.data["history"])

    def count_today(self):
        return sum(1 for h in self.data["history"] if h["day"] == today())

    # ---------- hints ----------
    def hints_used(self, slug):
        return self.data["hints_used"].get(slug, 0)

    def use_hint(self, slug):
        n = self.hints_used(slug) + 1
        self.data["hints_used"][slug] = n
        return n

    def reset_hints(self, slug):
        self.data["hints_used"].pop(slug, None)
