# Chapter authoring brief

You are writing one chapter of vim-dojo, a 585-lesson vim curriculum meant to be
worked through two lessons a day for a year. Repo root: `/home/peter/Projects/vim-dojo`.

## Read first, in this order

1. `docs/AUTHORING.md` — the format and the rules. All of it. It is the contract.
2. `curriculum.json` — find your chapter by its number. `teaches` is your scope
   and `skills` is the exact set of skill names you may use. Do not invent skills.
   `target` is how many lessons to write.
3. The three gold-standard exemplars. Match their depth, voice and structure:
   - `lessons/01-modes/01-01-first-contact.lesson` (a lesson)
   - `lessons/01-modes/01-03-escape-reflex.lesson` (a drill)
   - `lessons/09-verb-object/09-20-refund-window.lesson` (a scenario)
4. `.dojo/codebase/` — the sample TypeScript service. Borrow its domain
   (orders, customers, payments, refunds), naming and style for code files.

## Write

Your chapter directory already exists. Write `target` lesson files into it,
numbered `NN-01` upward with no gaps. Difficulty must climb across the chapter:
the first lesson assumes nothing beyond earlier chapters, the last is genuinely
demanding.

Composition for a chapter of ~18: roughly 12 `lesson`, 4 `drill`, and — for
chapter 8 and above — 2 `scenario`. Below chapter 8, use drills for the balance.

## Verify before you finish

You have a real vim and a real shell. Use them; do not guess.

1. `./dojo doctor` must report zero problems.
2. For **every** lesson, actually solve it in vim and confirm the keystroke
   count is at or under par. Script it like this and read the output:

   ```
   cd /home/peter/Projects/vim-dojo
   python3 - <<'PY'
   from engine.lesson import find
   from engine.runner import Attempt, KEYLOG
   import subprocess, pathlib
   l = find("04-07")
   att = Attempt(l); att.prepare(force=True)
   keys = pathlib.Path("/tmp/keys.in")
   keys.write_bytes(b"3jdd:wq\r")          # your intended solution, bytes; \x1b is Esc
   KEYLOG.unlink(missing_ok=True)
   subprocess.call(["vim","-s",str(keys),"-w",str(KEYLOG)] + l.open_files,
                   cwd=att.dir, stdout=subprocess.DEVNULL)
   ok, fails = att.check(verbose=False)
   print(l.id, "pass:", ok, "keys:", att.keystrokes(), "par:", l.par, fails)
   PY
   ```

   Vim prints terminal noise to stdout when driven this way; `stdout=DEVNULL`
   silences it. If a lesson fails or goes over par, fix the lesson, not the test.

3. Delete `.dojo/work` when you are done so you leave no scratch files behind.

## Report back

A short summary: how many lessons, their titles, any lesson where you had to
adjust par, and anything you think the next chapter's author should know.
Do not paste lesson content into your report.

## Do not

- Touch anything outside your own chapter directory.
- Run git commands.
- Use skills not listed for your chapter.
- Write a lesson whose solution needs a key taught in a later chapter.

## Gotchas found the hard way

Earlier chapter authors hit all of these. Do not rediscover them.

**Use `./dojo verify`, not your own harness.** It handles the scripting for you:

    ./dojo verify 04-07 '3jdd:wq\r'
    ./dojo verify 10-04 'ci"localhost\x1b:wq\r'

`\x1b` is Esc, `\r` is Enter, `\x16` is Ctrl-V. It prints pass/fail, the
keystroke count and whether the run tripped the arrow-key flag, and exits
non-zero if the lesson fails *or* goes over par. Loop it over your whole
chapter before you report back.

**`ZZ` at the end of a scripted solution does not get processed.** The file
is left unwritten and a correct solution looks like a failure. Append two
`\x1b` bytes after `ZZ` when verifying; they are not logged, so the
measured count stays honest.

**Backspace costs 3 bytes.** Vim logs it as `\x80kb`, not one byte. A
solution that leans on Backspace needs par padded accordingly. It no
longer trips the arrow-key flag — that was a grader bug and it is fixed —
but the byte cost is real.

**`-u NONE` means `backspace=""`**, so insert-mode Backspace cannot cross
the point where insert mode started. If a lesson needs it, set
`vimrc: set backspace=indent,eol,start` rather than relying on the
player's own config.

**More than one file in `open:` plus `ZZ` or `:q` hits E173** ("more files
to edit"). Until buffer switching is taught in chapter 16, multi-file
lessons must finish with `:wqa` — or just keep them single-file.

**Name your scratch files uniquely.** Several chapter authors run at once
and share a scratch directory. A file called `keys.in` will be overwritten
by somebody else's `keys.in` mid-run.

**Do not touch `.dojo/work/` belonging to other chapters.** Clean up only
the directories for your own lesson ids.

**Count motions in vim, not on paper.** Vim opens a file with the cursor on
the first non-blank character of line 1, but `j` preserves the column. A
counted motion from line 1 of an indented file is therefore one short of
the same motion made after a `j`. This off-by-one is very easy to ship.

**Know what the player does not have yet.** Chapters 1–5 give no delete
command at all, so before chapter 8 the only way to replace text is `ea`
followed by insert-mode `Ctrl-W`. Before chapter 16 there is no buffer
switching, so no multi-file lessons and no decoy files. Check the chapters
before yours and use only what they have handed over.

## Grader changes (read this — it affects your pars)

The keystroke counter has been corrected since the first wave. It now
reports what the player actually pressed:

- **`f`, `t`, `r` and `R` no longer cost three extra bytes.** Vim emits a
  bookkeeping byte after a character-pending read; the player never pressed
  it, so it is stripped. `f,` costs two keystrokes, not five. Earlier
  chapters set pars against the old inflated count, so their pars are
  slightly generous — yours should not be.
- **Backspace costs one keystroke and carries no penalty.** It used to cost
  three and to trip the arrow-key flag. It is a fair key; treat it as one.
- **Arrow keys, Home, End, Page Up/Down and the mouse still cost three
  bytes each and still lose the no-arrows badge.** That is deliberate. The
  arrow tax is a teaching device, not an accident — chapter 3 has a lesson
  built on it.

Set par from a measured `./dojo verify` run plus about 15%. Never from a
hand count.

## More gotchas, from the second wave

**Vim's TypeScript ftplugin continues comment leaders.** A counted `o` whose
text begins with `//` gets a second `//` on every repeat. Counted `o` is safe
in `.md`, `.csv` and `.sql`. Inside a TypeScript array or object literal,
autoindent already supplies the indentation, so the text you have the player
type must not include leading spaces.

**`:wq` with more than one file in the arglist raises E173** and does not
advance. Either use `:wn` to step through them, `:wqa` to write and quit
everything, or leave the extra files unopened.

**Never grade on anything that depends on terminal width.** A lesson may
*teach* wrapped-line movement, but the expected file has to be reachable at
any width. Break lines at sentence boundaries the player can search for, not
at wrap columns. If the route's length varies with width, set par loosely and
say so in the solution.

**Options go through the `vimrc` meta field, never through instructions to
the player.** `vimrc: set relativenumber` is reproducible; "first, run
`:set relativenumber`" is not, and it costs the player keystrokes that the
par did not budget for.

## Undo lessons need `--slow`

`vim -s` never idles, and vim only closes an undo block when it idles
waiting for input. Fed a script, every consecutive insert session merges
into one undo step, so `u` wipes them all and a correct undo lesson looks
broken. Any lesson about undo granularity, counts on `u`, `U`, `:earlier`,
`g-` or `:undo N` must be verified with:

    ./dojo verify --slow 02-06 '...'

which types through a real terminal with a pause after every Esc and Enter.
It takes a few seconds per lesson. Plain `./dojo verify` is fine for
everything else.

## Isolation (fixed — but know it)

Each attempt now keeps its keystroke log and its undo history inside its
own work directory, so parallel authors can no longer contaminate each
other's counts, and a replay can no longer inherit the undo tree of the
attempt it replaced. If you wrote your own harness against the old shared
`.dojo/keys.log`, throw it away and use `./dojo verify`.

## The player's vimrc (verified, not assumed)

The dojo runs plain `vim`, which loads `~/.vimrc`. These are set there and
`./dojo verify` runs under them too:

- `ignorecase` + `smartcase` — `/users` matches `UserService`. A search
  that must land on an exact lowercase word needs distinguishing context
  (`/\/users\/`, `/response\.`) or `\C`. This has already caused one
  capstone solution to land on the wrong line.
- `hlsearch`, `incsearch`, `number` (not `relativenumber`).
- `hidden` — `:bn` leaves a modified buffer without complaint. Do not
  rely on it either way: `:w` before switching is the honest habit.
- `mouse=a` — mouse clicks are logged and cost the badge. That is the point.
- `clipboard=unnamedplus` — `y` and `p` go through the system clipboard.
  Under `./dojo verify` this is inert; in a real session an external copy
  can end up in the unnamed register. Chapter 20 should teach `"0` for
  exactly this reason.
- `autoindent`, `expandtab`, `shiftwidth=2` — `o` and `O` supply the indent;
  typed text must not include leading spaces.
- `undofile` — now harmless, since each attempt has its own undo directory.
- `backspace=indent,eol,start`.

A lesson must pass under these settings. A lesson that *depends* on one of
them should set it explicitly through the `vimrc` meta field anyway, so it
also passes on a machine without this config.

## Backslashes in `./dojo verify`

The keystroke spec understands exactly these escapes: `\xHH`, `\r`, `\n`,
`\t`, `\e` (Esc) and `\\` (one literal backslash). **Every other backslash
goes to vim untouched**, so vim patterns are written naturally:

    ./dojo verify 13-04 '/\<order\>\rciwrefund\e:wq\r'
    ./dojo verify 14-09 ':%s/\v(\w+), (\w+)/\2 \1/g\r:wq\r'

Do not double backslashes for vim's sake. Do not use the bytes-literal form
unless you need something the escapes above cannot express.

**`j` keeps the column, and `f` only looks forward.** After an edit that
leaves the cursor far along a line, `j` lands far along the next line too,
and `f<char>` then silently misses anything to the left. Put `0` after `j`
whenever the next move is a find. This was the single biggest cause of
failed verify runs in chapter 8.

**Multi-file lessons that switch buffers need `vimrc: set hidden`**, or an
explicit `:w` before every switch. Without one of those, `:bn` from a dirty
buffer raises E37 and the whole solution derails from that point.

**`:g//normal` starts each line in column 1**, not on the first non-blank,
so `dw` there eats the indentation. Begin the normal sequence with `^` or
`_` when it matters.

**Looping `./dojo verify` in a `while read` loop:** redirect the verify
call's stdin from `/dev/null`, or vim swallows the rest of the loop's input
and only the first lesson runs.

**`dap` and blank lines inside a body.** A method with a blank line in its
body is two paragraphs to vim; `dap` from the top takes only the first.
Either write single-statement bodies for the thing being deleted, or teach
`d}` twice. Do not tell the player `dap` takes the whole method when it
does not — verify it.

**The `c` confirm flag under `./dojo verify`:** supply exactly one answer
(`y`/`n`/`a`/`q`/`l`) per match, no more, no fewer. A leftover key is eaten
by the confirm prompt — the `q` of a trailing `:wq` becomes "quit
confirming" and vim never exits, so the run hangs. Count the matches in
vim (`:%s/pat//gn`) before writing the spec.

## More, from the buffers/finding-files wave

**netrw's `%` and `d` call `inputsave()`**, which clears typeahead, so a
plain `./dojo verify` run is swallowed. Any lesson that creates a file
through netrw needs `--slow`, and can still race the prompt on a loaded
machine. Prefer `:e path/to/new.ts` for creating files unless netrw's `%`
is itself the lesson.

**In a netrw listing, `/name` + Enter only finishes the search** — a second
Enter opens the file. Do not count `j` presses to reach an entry: the
attempt's own `.keys.log` and `.undo/` appear in the listing, and netrw
prints the absolute work path in its header, so a lesson slug containing a
word you search for will match the header line.

**`:vs name` opens the new window on the LEFT** with the cursor in it,
because `splitright` is off.

**`:q` or `:wq` in a split closes only that window** and the script carries
on in the remaining one. If a scripted solution ends with vim still open,
`./dojo verify` hangs. While experimenting, append `:qa!\r` as a safety
net, then remove it before measuring.

**`:find` completion is a prefix match** on the file name; `*fragment`
makes it a substring match. Under `wildmode=longest:full,full` the first
Tab on an ambiguous fragment inserts nothing and only shows the bar; the
second Tab picks the first candidate alphabetically by full path.

**If a verify run hangs**, find the stray process by its `-w` path
(`pgrep -af '^vim'`) and kill that one. Anchor the pattern with `^vim` or
you will match your own shell command.

## viminfo is now isolated too (supersedes an earlier warning)

Each attempt gets its own `.viminfo`, so the jumplist, changelist, marks
and registers start empty every time and the dojo no longer writes into
the player's own `~/.viminfo`.

Consequences, if you read an older note saying otherwise:

- `:jumps`, `:changes` and `:marks` are safe in a scripted route. They used
  to hit a `-- More --` prompt from ~100 inherited entries and abort the
  run. You no longer need to pad par for dismissing them.
- `Ctrl-O` past the first jump stays in the lesson's files instead of
  walking off into a file from a previous session.
- Registers do not carry over between attempts, so a lesson may rely on a
  register being empty at the start.

**Cross-file `Ctrl-O` and `` `A `` silently stay put** when the current
buffer is modified and `hidden` is off. Cross-file lessons should set
`vimrc: set hidden` and finish with `:wqa`.

**Under plain `-s` every change collapses into one changelist entry**, so
anything touching `g;`, `g,`, `` `. `` or `` `^ `` must be verified with
`--slow`.

**Blockwise `I` inserts at the block's left edge**, which is wherever the
column started — not the first non-blank. Start the block with `^` (or from
the right column) or every line gets the text in the margin.

**In blockwise, `$` must come after the block has its height.** `$` then `G`
drops the ragged flag and `A` pads to a fixed column instead of appending at
each line's own end.

**Clean up only your own scratch files, by exact name.** A glob like
`rm -f k*` in the shared scratchpad can take another running author's files
with it.

**If your chapter needs a skill `curriculum.json` does not list, say so in
your report** rather than tagging lessons with the nearest thing that fits.
The skill list drives spaced repetition: a mis-tagged lesson schedules
review for the wrong thing. Chapter 24 needed `ex-sort` and `cmdline-edit`;
both have since been added.

**`q:` under `./dojo verify`** opens with the cursor on the empty new-command
line at the bottom, so a scripted edit must start with `k` to reach the last
real command. `G` lands on the blank line and the edit silently does nothing.

## The unnamed register is now private (and why)

The runner starts vim with `set clipboard=`. The player's own vimrc sets
`clipboard=unnamedplus`, and with a live X display that makes the unnamed
register *the system clipboard* — so a plain `p` could put whatever another
program copied a moment ago, and parallel authors' vims were writing into
each other's. One author observed another's code sitting in `"+` mid-run.

What this means for you:

- Plain `y`/`d`/`p` are deterministic. Write solutions with confidence.
- `"+` and `"*` still reach the real system clipboard, so lessons that
  teach clipboard integration work unchanged.
- A lesson that genuinely needs `unnamedplus` behaviour must set it back
  through its own `vimrc` field, and should not be graded on it.

**`vimrc: let @a="...\n" | let @b="...\n"`** works as a single `-c` and
pre-loads registers before the player arrives — the way to build a lesson
about reading `:reg`, or about editing a macro already sitting in `"q`.

**Redirect stdin when scripting verify runs:** `./dojo verify … </dev/null`.
Without it, a run that ends in a recursive macro or an over-count can
consume the rest of your shell input and produce no output file. This is
reliable with the redirect and flaky without it.

**A charwise `"ap` leaves the cursor at the END of the pasted text**, so a
following `f<char>` searches from there and misses. Put `0` first.

**`s` and `x` clobber the unnamed register.** A macro that yanks and then
replaces must delete first and yank second, or the yank is lost.

## The work directory now contains only lesson files

The keystroke log, undo history, viminfo and the verify script used to sit
in the lesson's working directory — which is vim's cwd, so the lesson could
see them. netrw listed them, `:find` completed them, and `:grep -r pat .`
matched the script and then `:cdo` edited it mid-read. They now live in a
sibling `.harness/` directory outside the player's view.

Even so, prefer `src` or an explicit glob over `.` in a grep lesson: it is
what a real engineer types, and it keeps the list to files the lesson owns.

**Other quickfix findings worth reusing:**

- `errorformat` set through the `vimrc` field needs a doubled backslash for
  its commas: `set errorformat=%f(%l\\,%c):\ %m`. A single `\,` arrives as
  a plain comma and every line loads as a message with no file attached.
- `:cdo` does not abort on E486 when a pattern is missing from one entry, so
  a substitution across a list is safe. `:normal` swallows `|`, so pair it
  with `:wa` rather than `| update`.
- `grep -r` returns hits in directory-walk order, not sorted, so a scripted
  `:cn` walk over a `:grep` list is not reproducible. Use `:cdo`.
- `:vimgrep **/*.ts` sorts `foo.test.ts` before `foo.ts`, so a decoy in a
  test file is hit first.
- `:wq` with the quickfix or location window open leaves vim running. Any
  solution with a list window open must end in `:wqa` or `:qa`.

## Comment leaders continue themselves (this has caught three chapters)

Vim's ftplugins continue the comment leader on `o`, `O` and Enter-in-insert:
`//` in TypeScript, `"` in `.vim` files, `--` in Lua. Open a line from a
comment and vim helpfully prefixes the new one too, so a typed code line
silently acquires a `-- ` and the expected file no longer matches.

The rule that works: **never open a new line from a comment line.** Type the
code first and add the comment above it with `O` from a non-comment line, and
shape the start file so that route is available. A counted `o` whose text
begins with a comment marker is doubly affected — it repeats the leader on
every line.

## Shell filters

**Design every `sort`/`ls`-graded lesson to be locale-insensitive.** This box
is `en_US.UTF-8`, which sorts case-insensitively and ignores punctuation;
`LC_ALL=C` does not, and a player elsewhere may have either. Keep sorted
blocks single-case with punctuation in the same position, then re-run the
lesson under `LC_ALL=C ./dojo verify …` and confirm identical output. The
harness deliberately does **not** pin the locale: the point of the dojo is
the player's real environment.

**A filter whose command exits non-zero costs an extra Enter.** `:%!grep NOPE`
empties the range *and* raises a `shell returned 1` hit-enter prompt that
swallows the next key. Budget par for it and include the extra `\r`.

**`:term` needs `--slow`.** Scripted input never reaches the terminal job
under plain verify and vim hangs until timeout.

**`.` repeats a filter**, including the whole command text.

**Check a tool exists before building a lesson on it.** `jq` (1.8.1),
`column`, `sort`, `uniq`, `tr`, `sed`, `awk`, `cut`, `wc`, `python3` and
`git` are present. `prettier`, `ctags` and `nvim` are **not** — mention them
in prose if useful, never grade on them.

**Swap files now live in the harness directory too.** A vim killed mid-run
used to leave a `.file.swp` in the work directory, and every later scripted
run then died on E325 with no visible message. If you are on an older
checkout and runs start failing inexplicably, `find . -name '.*.sw*' -delete`.

**A hand-written `tags` file works perfectly** and is the way to teach
go-to-definition without ctags: tab-separated `name<TAB>file<TAB>/^pattern$/;"<TAB>kind`,
sorted, with a `!_TAG_FILE_SORTED	1` header. Duplicate names are numbered by
`:tselect`/`g]` in tags-file order, so you can deliberately make `Ctrl-]`
pick the wrong one and teach the fix.

**`%-G\ %.%#` must be the FIRST pattern in an `errorformat`** that drops a
compiler's indented "related information" lines. Put it last and the
file/line pattern matches them first.

**`:vert diffsplit file` opens the new window on the LEFT** with the cursor
in it, so a scripted route needs `Ctrl-W l` before any `do`/`dp` or you edit
the wrong side.

**Do not grade on `git` commands run from a lesson.** The work directory sits
inside the dojo's own repository, so `:!git diff` acts on that repo and its
output is not deterministic. Teach git in prose and `@keys`, and grade
against a provided `.orig` file or plain conflict-marker text.

## `:normal` and the bar

**`:normal` swallows a following `|`.** `:argdo /a/,/b/normal @q | update`
does not run `update` — the characters `| update` are fed to normal mode
(undo, put, …) and the run then hangs waiting for input. Wrap it:

    :argdo execute "/a/,/b/normal @q" | update

`:bufdo %s/…/ge | update` is fine, because `:s` does not eat the bar.

**`:normal` only closes insert mode at the end of each line.** A mid-sequence
Esc has to go through `:execute` with a double-quoted string and `\<Esc>`.

**A guarded macro survives `:normal` over an already-converted line.** Start
the macro with a motion that fails on a converted line (`0f;`) and the keys
abort for that line only while the range loop carries on — which is what
makes "record once, apply to everything including the row you recorded on"
work.

**Check the actual output, do not reason about it.** Look in
`.dojo/work/<slug>/` after a failed run. Deleting a block with a blank line
on both sides leaves two blank lines, and an `@expected` written by eye will
not match. This cost two authors a failed verify each.

**`ci{` works outwards from the cursor**, unlike `ci'` and `ci"` which search
forward on the line. Aimed at an empty `{}` further along the line, `ci{`
takes the enclosing block instead. Put an `f{` first.

## Verify the negative case too

If a lesson has a trap — a hit that must not be replaced, a setting that must
be diagnosed first, a `| update` without which nothing saves — then also run
the route that *skips* it and confirm the lesson fails. A trap that does not
fire is worse than no trap: it teaches the player that the careless route is
fine. Chapter 19, 27 and 28 all did this; it is cheap and it is the difference
between a lesson and a decoration.

And if a lesson's premise turns out to be false when you test it, cut the
lesson. One author built a lesson on `gg=G` behaving differently with and
without a filetype set; it does not, because the fallback C-indent handles
that code identically. Dropping it was right.

## Options, autocommands and mappings

**The `vimrc` field arrives as a `-c`, after the first file is loaded** and
after its ftplugins have run. A `BufRead` or `FileType` autocommand set there
will never fire for the file already open. Use `vimrc: source config.vim|e` —
the `|e` reloads the buffer so the autocommands run normally.

**Shipping a `config.vim` in `@start` with no `@expected` twin** is a strong
pattern for this material: the player reads the offending config, `:verbose
set` names it by absolute path and line, and the decoy rule stops them
"fixing" it by editing it.

**`:wqa` only writes buffers that have been loaded**, and vim loads only the
first file of the arglist. An autocommand meant to touch every file needs
`:argdo w` then `:qa`.

**A mapping's rhs cannot contain a literal Esc** typed on the command line —
it cancels the command line. Spell it `<Esc>`.

**A recursive mapping (`nmap x "_x`) hangs vim under `-s`** rather than
erroring. Never verify a route that presses the un-fixed key.

## Shipping a real plugin with a lesson

It works, and it is the honest way to teach plugins with no network. Ship the
plugin as `@start pack/dojo/start/<name>/plugin/<name>.vim` with no
`@expected` twin, so the grader also enforces that the player leaves the
source alone, and say in the brief that it came with the lesson.

The incantation is `vimrc: set packpath^=. | packloadall!` — **the bang is
required**. Plain `:packloadall` is a no-op because vim already ran it at
startup, and the package silently never loads.

Useful facts that follow:

- `getchar()` inside a mapping or `operatorfunc` reads from the `-s` script,
  so `ys{motion}{char}`-style plugins are verifiable.
- `:helptags ALL` output is byte-deterministic and can be graded as an
  `@expected` file; `packloadall!` puts a package's doc directory on
  `runtimepath` so it is reachable.
- `matchfuzzy()` is built into vim 9.1, so a usable fuzzy finder is ~30 lines.
- `commentstring` on this machine: ts/js `// %s`, sql `-- %s`, markdown
  `<!-- %s -->`, yaml/sh/python `# %s`, vim `"%s`, and **json is empty** —
  a good gap to build a lesson on.
- `git diff --no-index -U0 a b` is deterministic with no repository, so it
  can be graded. `git log` or `git ls-files` in the work directory cannot —
  that directory sits inside the dojo's own repo.
- **`va"` swallows adjacent whitespace**, so "strip the first and last
  character" is the wrong model for a surround-like plugin. Use `yi"` for the
  inner text and `vi"ohol` to select the pair.

## If a brief claims a number, measure both routes

The final boss originally told the player "typing this out by hand is about
900 keystrokes" with par at 700. The slow route actually measures 610, so it
passed comfortably and the lesson's whole point — copy the method, do not
retype it — was enforced by nothing. Par is now 500: the copy route measures
382, the typing route 610.

Whenever a lesson's brief or solution asserts that one route is cheaper than
another, **measure both** and put the real figures in the text. A par that
does not exclude the route you are arguing against is decoration.

**`:g` leaves the cursor on the last line it acted on**, so a `/search` after
a `:g` starts from there and not from where you were. Add a `gg` first.

**After a linewise `p` the cursor sits at column 0 on whitespace**, so `ww`
reaches the second word of the line, not the method name. Count it in vim.
