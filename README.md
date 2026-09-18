# vim-dojo

585 lessons. Two a day, for a year.

You cannot finish this in a weekend, and that is the point. Vim is not a
feature list to be read once — it is a motor skill, and motor skills are
built by short, repeated, slightly uncomfortable practice over months.
The dojo is built to enforce that rhythm rather than let you binge it.

Every lesson is a real editing job on a realistic TypeScript codebase,
checked against an expected result, scored on keystrokes, and flagged if
you touched an arrow key or the mouse.

## Start

```sh
cd vim-dojo
./dojo            # what to do today
./dojo play       # the next lesson
```

`./dojo play` prints the mission and opens vim with the right files.
Do the work, `:wq`, and it grades you the moment vim closes.

If vim ever traps you: `Esc`, then `:q!` and Enter leaves without saving.

## The day

```
./dojo            what to do today, and your streak
./dojo review     spaced repetition — whatever has gone stale
./dojo play       new ground
./dojo drill      the same edit ten times, against the clock
./dojo scenario   a real multi-file job
```

A good session is fifteen minutes: clear the review queue, do one or two
new lessons, and drill whatever the dojo says is shakiest. Doing eight
lessons on a Sunday and none for a fortnight will teach you less than
fifteen minutes on six days.

## When you are stuck

```
./dojo hint       one nudge at a time, three per lesson
./dojo keys       just the keys this lesson is about
./dojo solution   the answer, and why it is the fast way
./dojo brief      re-read the mission
./dojo cheat      the VS Code -> vim cheatsheet
```

Reading the solution is not cheating. Reading the solution and then
running `./dojo replay` until you beat par is the entire method.

## Tracking

```
./dojo map        the whole curriculum, or one chapter: ./dojo map 14
./dojo stats      progress, streak, strongest and shakiest skills
./dojo skills     every skill and when it next falls due
./dojo goto 14-03 jump to a lesson or chapter
./dojo replay     wipe this lesson and do it again, faster
```

## How the grading works

Three numbers, and they matter in this order.

**Correct.** Your file is compared to the expected file. Trailing
whitespace and the final newline are ignored; nothing else is.

**Keystrokes.** Vim logs every key you press, and the log is measured
against a par set from the intended solution. Under par means you found
the intended route or better. Way over par means you brute-forced it,
and it will tell you to read the solution and replay.

**Clean.** Arrow keys, Home, End, Page Up/Down and the mouse all leave a
distinctive mark in the key log. A run without them earns a badge. This
is deliberately strict: the arrow keys are the single habit that stops
VS Code refugees from ever getting fast.

## The belts

| | belt | | chapters |
|---|---|---|---|
| **Survival** | white | Stop being afraid of the editor | 1–3 |
| **Movement** | yellow | Never touch an arrow key again | 4–7 |
| **The grammar** | orange | Verb plus object, and the multiplication that follows | 8–11 |
| **Search and replace** | green | Change what you cannot see, safely | 12–15 |
| **Many files** | blue | Move through a codebase without losing your place | 16–19 |
| **Power tools** | purple | Registers, macros, blockwise editing | 20–23 |
| **Ex and automation** | brown | The command language under the editor | 24–27 |
| **Mastery** | black | Your own config, plugins, LSP, and real engineering work | 28–32 |

`./dojo map` shows every chapter and how much of it you have cleared.

## Spaced repetition

Each lesson declares the skills it exercises. When you clear one, those
skills get a review date, scheduled by how well you did: fluent and under
par pushes it weeks out, a struggle brings it back tomorrow. `./dojo
review` replays the lessons whose skills have gone stale.

This is the part that makes a year's worth of material stick rather than
wash over you. Chapter 21 is useless to you in March if you last saw
chapter 10 in January and never went back.

## Using it for real

The dojo teaches the moves. Only daily use makes them automatic.

- `export EDITOR=vim` so git drops you into vim for commit messages.
- Edit your configs, your notes, your scratch files in vim even when it
  is slower. It is only slower for about three weeks.
- When you catch yourself doing something tediously, stop and look it
  up — `:h` inside vim, or `./dojo cheat`. That single habit is the
  difference between two weeks and two years.
- Add one line to your vimrc at a time, when something annoys you. A
  copied 500-line config teaches you nothing. Chapter 28 is about
  building your own.

## The one thing to remember

Normal mode is home. Insert mode is somewhere you visit to type, then
leave. If you are ever confused, press `Esc` and you are back on solid
ground.

## Writing lessons

The curriculum lives in `curriculum.json`, lessons in `lessons/`, one
plain-text file each. `docs/AUTHORING.md` is the format and the house
rules; `./dojo doctor` validates every lesson file.
