# vim-dojo

Fourteen levels. Each one is a real editing job on a realistic TypeScript
codebase, checked against an expected result and scored on keystrokes.

    ./dojo            where you are
    ./dojo play       read the mission, open vim
    ./dojo check      grade it
    ./dojo hint       one nudge at a time
    ./dojo keys       the keys this level is about
    ./dojo solution   the answer, when you want it
    ./dojo replay     wipe this level and do it again, faster
    ./dojo goto 7     jump to a level
    ./dojo cheat      the VS Code -> vim cheatsheet

`./dojo play` drops you into vim with the level's files already open.
When you `:wq` out of it, the checker runs automatically.

## The belts

| | | translates from |
|---|---|---|
| 1 | Survival: modes, save, undo | typing, Ctrl+S, Ctrl+Z |
| 2 | Moving without arrow keys | arrow keys, Ctrl+Home |
| 3 | Delete, copy, paste, change | Ctrl+X/C/V |
| 4 | The grammar: verb + object | double-click, Ctrl+D, F2 |
| 5 | Sniping inside one line | clicking precisely |
| 6 | Searching inside a file | Ctrl+F |
| 7 | Find and replace, with judgement | Ctrl+H |
| 8 | Visual mode and the column trick | Alt+click multi-cursor |
| 9 | Getting back where you were | Alt+Left, F12 |
| 10 | Many files, one window | tabs, split editor |
| 11 | Opening a file by name | Ctrl+P |
| 12 | Search the repo, fix every hit | Ctrl+Shift+F |
| 13 | Record once, replay forever | nothing - vim only |
| 14 | Boss: a feature in four files | a normal afternoon |

## How to actually get good at this

Levels teach the moves. Only daily use makes them automatic, so:

- **Do one level a day, not all fourteen tonight.** The bottleneck is
  finger memory, not understanding.
- **Replay levels.** `./dojo replay` after reading the solution is where
  the keystroke count drops. Beating par matters more than clearing.
- **Use vim for something real between levels** - commit messages,
  editing a config, notes. Set `export EDITOR=vim` so git drops you
  into it.
- **When you catch yourself doing something tediously, stop and look it
  up.** `:h` inside vim, and the cheatsheet here. That habit is the
  whole difference between two weeks and two years.
- **Add one line to your vimrc at a time**, when something annoys you.
  A copied 500-line config teaches you nothing.

## The one thing to remember

Normal mode is home. Insert mode is a place you visit to type, then
leave. If you are ever confused, press Esc and you are back on solid
ground.
