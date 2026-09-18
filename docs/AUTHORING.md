# Writing lessons for vim-dojo

Read this whole file before writing a single lesson. Every lesson you write is
graded by `./dojo doctor` and, more importantly, by a real person who is new to
vim and trusts the dojo not to waste their time.

## The reader

One person: a working developer, competent, coming from VS Code. They are not a
beginner at programming — never explain what a function is. They *are* a beginner
at vim, and their instinct when confused is to reach for the mouse. Every lesson
should make the mouse feel slower than the keyboard.

They are doing this for a year, two lessons a day. That means the ~585 lessons
must not repeat each other. Check the chapter's `teaches` line in
`curriculum.json` and stay inside it.

## File layout

One lesson per file: `lessons/<NN>-<chapter-slug>/<NN>-<MM>-<lesson-slug>.lesson`

    lessons/10-text-objects/10-04-inner-quotes.lesson

`NN` is the chapter number from `curriculum.json`, `MM` is the lesson's position
in the chapter, both zero-padded. The id is `NN-MM`.

## Format

Sections start with `@name` at column 0.

```
@meta
id: 10-04
title: Change what is inside the quotes
chapter: 10
type: lesson
skills: obj-quote, inner-vs-around
par: 26
minutes: 4
vscode: double-click inside the string, retype it
open: config.ts

@brief
Prose. What the job is, and the one idea behind it.

@keys
| `ci"` | change inside the quotes |

@hints
The first nudge — a direction, not an answer.
--
The second — names the key but not the sequence.
--
The third — near enough to the solution to unblock anyone.

@solution
The keystrokes, then why they are the fast way.

@start config.ts
export const config = {
  host: 'locahost',
}

@expected config.ts
export const config = {
  host: 'localhost',
}
```

### meta fields

| field | required | notes |
|---|---|---|
| `id` | yes | `NN-MM`, unique across the whole dojo |
| `title` | yes | Sentence case, no trailing period, under 46 characters |
| `chapter` | yes | matches the directory |
| `type` | yes | `lesson`, `drill`, `scenario` or `boss` |
| `skills` | yes | comma separated, from your chapter's list in `curriculum.json` or any **earlier** chapter's — never a later one |
| `par` | yes | see below |
| `minutes` | no | honest estimate, default 4 |
| `vscode` | no | what they'd have done in VS Code. Powerful — use it whenever there is an equivalent |
| `open` | no | space separated, the files vim opens with and in what order |
| `reps` | drills | how many repetitions, 6–12 |
| `vimrc` | rare | a single `-c` command, e.g. `set path=.,**` when the lesson needs it |

### Setting par

Par is a byte count of the keystroke log, and it includes `:wq` plus Enter
(4 bytes). Work out the intended solution, count its characters, add the 4, then
add about 15% of slack. A lesson whose par is impossible is worse than no lesson.
Sanity check: a one-word fix is par 12–20; a whole-file refactor is par 120–300.

## The rules that make or break a lesson

1. **One new idea per lesson.** Everything else in it must already have been
   taught in an earlier chapter. If you need something from a later chapter,
   the lesson is in the wrong place.
2. **Real code, real text.** Files come from a plausible TypeScript service, a
   config, a markdown doc, a log, a CSV. Never `foo bar baz`. There is a sample
   codebase at `.dojo/codebase/` — borrow its style, naming, and domain
   (orders, customers, payments).
3. **The file must make the slow way painful.** If the lesson can be finished
   just as fast by typing, it teaches nothing. Twenty lines of near-identical
   text is what makes a macro obviously right.
4. **Grade exactly what you teach.** The expected file must differ from the
   start file *only* in the ways the lesson is about. No incidental whitespace
   changes, no reordering.
5. **The brief says what, never how.** Describing the outcome is the lesson;
   naming the keys is the solution. Keys go in `@keys` and `@hints`.
6. **Three hints, escalating.** First a direction, then the key's name, then
   close to the answer. Someone stuck at 11pm must be able to get unstuck.
7. **The solution explains the why.** Not just `ci"` — *why* the text object
   beats selecting by hand, and what else it generalises to.
8. **Never require a plugin** before chapter 29. Plain vim 9, no config, except
   through the `vimrc` meta field.
9. **Trailing whitespace and the final newline are normalised away** by the
   grader. Never build a lesson around either.
10. **Decoy files are allowed and encouraged.** A file listed in `@start` with no
    `@expected` twin must be left untouched — the grader fails the player if they
    change it. This is how you teach precision.

## Voice

Plain, direct, a bit dry. Short sentences. Second person. No exclamation marks,
no emoji, no "Congratulations!", no motivational filler. The tone of a good
colleague showing you something over your shoulder.

Good: "A blind replace-all breaks the customer-facing string. That exception is
the whole lesson."

Bad: "Great job! Now let's learn about the amazing power of substitution! 🚀"

## The four types

**`lesson`** — the default. Teach one idea, apply it once, grade the file.

**`drill`** — the same short edit repeated. Set `reps: 8`, keep the file small
and the edit under five seconds for someone fluent. The brief is one or two
lines; there is nothing to think about, that is the point. Skip the third hint.

**`scenario`** — a job, not an exercise. Three to six files, framed as a ticket:
"Orders placed before the cutoff are being charged twice. Fix it and update the
test." Skills are drawn from several earlier chapters. These are where a player
finds out whether any of it stuck.

**`boss`** — a scenario at chapter scale, one per belt, deliberately long.

## Checklist before you hand a chapter over

- `./dojo doctor` passes with zero problems.
- Every lesson's `skills` come from your chapter or an earlier one. A plain
  lesson should stay inside its own chapter's list; only scenarios, capstones
  and bosses should reach back.
- Ids are contiguous: `NN-01` through `NN-<target>`, no gaps, no duplicates.
- You have actually solved each lesson yourself in vim and the keystroke count
  is under par.
- No two lessons in the chapter are the same exercise with different words.
- At least two drills and, from chapter 8 onward, at least one scenario.
