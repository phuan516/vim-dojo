# VS Code -> vim

Everything here is plain vim 9, no plugins.

## The daily ten

| VS Code | vim |
|---|---|
| Ctrl+S | `:w` |
| Ctrl+Z / Ctrl+Y | `u` / `Ctrl-R` |
| Ctrl+F | `/text` then `n` / `N` - or `*` on the word under the cursor |
| Ctrl+H | `:%s/old/new/g` (add `c` to confirm each) |
| Ctrl+P | `:find name.ts` (needs `set path=.,**`) or `:b partialname` |
| Ctrl+Shift+F | `:vimgrep /x/ **/*.ts` then `:copen`, `:cn` |
| Ctrl+D multi-cursor | `*` then `cgn`, then `.` `.` `.` |
| Alt+click column edit | `Ctrl-V`, move, `I` or `A`, type, `Esc` |
| Alt+Left (go back) | `Ctrl-O` (`Ctrl-I` forward) |
| F2 rename symbol | `:%s/\<old\>/new/gc`, or `:cdo` across files |

## Moving

| | |
|---|---|
| `h j k l` | left down up right |
| `w` `b` `e` | word forward / back / end of word |
| `0` `^` `$` | line start / first real character / line end |
| `f x` `t x` | to the next `x` on this line / just before it; `;` repeats |
| `gg` `G` `42G` | top / bottom / line 42 |
| `{` `}` | up / down a paragraph |
| `Ctrl-D` `Ctrl-U` | half a screen down / up |
| `%` | matching bracket |
| `zz` | centre the screen on the cursor |

## Changing - verb + object

Verbs: `d` delete  `c` change  `y` yank  `>` indent  `gU` upper case

Objects: `w` word  `iw` inner word  `i"` inside quotes  `i(` `i{` `i[`
inside brackets  `it` inside a tag  `ap` a paragraph  `$` to end of line

So: `diw` `ci"` `ya(` `d$` `>ip` `gUiw`. Doubling the verb does the
line: `dd` `yy` `cc`.

| | |
|---|---|
| `x` `r` | delete one char / replace one char |
| `i` `a` `I` `A` | insert here / after / at line start / at line end |
| `o` `O` | new line below / above |
| `p` `P` | put after / before |
| `.` | repeat the last change - the most underused key in vim |
| `J` | join this line with the next |

## Files and windows

| | |
|---|---|
| `:e path` | open a file |
| `:ls` | list buffers |
| `:b name` | switch to a buffer by partial name |
| `Ctrl-^` | flip to the previous file |
| `:vs` `:sp` | vertical / horizontal split |
| `Ctrl-W h j k l` | move between splits |
| `Ctrl-W o` | close all splits but this one |
| `:wa` `:qa` `:wqa` | write all / quit all / both |
| `gf` | open the file named under the cursor |

## Macros

`qa` record into `a` · `q` stop · `@a` play · `7@a` play seven times ·
`@@` play the last one again · `:reg a` see what you recorded

Record from a predictable spot, end with `j`, and re-record rather than
repair.

## Registers

`"ayy` yank into register a · `"ap` put from a · `"+y` yank to the system
clipboard (your vimrc already makes `y` do this) · `"0p` put the last
*yank*, ignoring anything you have deleted since - the fix for "my paste
got clobbered by a delete".

## When stuck

- `Esc` - always safe, always takes you back to normal mode.
- `u` - undo. `:earlier 10m` - the file as it was ten minutes ago.
- `:q!` - leave without saving.
- `:h ciw` - help for any command. `:h` alone is a genuinely good manual.
- `vimtutor` in your terminal - the official 30-minute walkthrough.

## Worth adding to ~/.vimrc when each one bites you

    set path=.,**            " makes :find work like Ctrl+P
    set relativenumber       " makes 5j / 12k obvious at a glance
    set splitright splitbelow
    nnoremap <Space> :
    " jk to leave insert mode without reaching for Esc:
    inoremap jk <Esc>

---

# Beyond the basics

Everything below is plain vim 9. Chapter numbers point at where the dojo
teaches it properly.

## Text objects (ch 10)

`i` = inner, `a` = around (includes the delimiter or trailing space).

| | |
|---|---|
| `iw` `aw` | word / word plus its trailing space |
| `iW` `aW` | WORD — whitespace-delimited, punctuation included |
| `i"` `a"` `i'` `` i` `` | inside / around quotes |
| `i(` `i)` `ib` | inside parentheses |
| `i{` `i}` `iB` | inside braces |
| `i[` `i]` | inside brackets |
| `i<` `i>` | inside angle brackets |
| `it` `at` | inside / around an HTML or JSX tag |
| `ip` `ap` | paragraph |
| `is` `as` | sentence |

Combine with any operator: `ci"` `da(` `yi{` `>ip` `=i{`.

## The dot command (ch 11)

`.` repeats the last change. Design edits so it works:

| instead of | do |
|---|---|
| select and retype each hit | `*` then `cgn` new text `Esc`, then `.` `.` `.` |
| `xxxxx` | `5x`, or better `dw` |
| retyping the same suffix | edit once, then `.` on the next one |

`;` repeats the last `f`/`t`. `&` repeats the last `:s` on this line.

## Regex dialect (ch 13)

| | |
|---|---|
| `\v` | very magic — regex behaves like every other tool you know |
| `\<` `\>` | word boundaries |
| `\zs` `\ze` | start / end the *match* here, matching context without replacing it |
| `\{n,m}` | quantifier (escaped brace in normal magic) |
| `\(...\)` | group in normal magic, `(...)` under `\v` |
| `\1` `\2` | backreferences, in pattern and replacement |
| `\c` `\C` | force case-insensitive / case-sensitive for this pattern |

## Substitute (ch 14)

```
:%s/old/new/g          whole file, every hit on each line
:%s/old/new/gc         confirm each one
:5,20s/old/new/        lines 5 to 20
:'<,'>s/old/new/       the visual selection
:%s/\<id\>/key/g       whole words only
:%s/(\w+), (\w+)/\2 \1/    swap, under \v
:%s/x/\=line('.')/g    replace with the result of an expression
:%s//new/g             reuse the last search pattern
```

Flags: `g` all on the line, `c` confirm, `i` ignore case, `e` no error if
not found, `n` count matches without changing anything.

## The global command (ch 15)

```
:g/TODO/d              delete every line containing TODO
:v/keep/d              delete every line NOT containing keep
:g/^$/d                squash blank lines
:g/error/normal A;     append a semicolon to every matching line
:g/pattern/t$          copy matching lines to the end
:g/pattern/m0          move matching lines to the top (reverses them)
```

`:g` plus `:normal` plus a macro is the closest vim gets to a scripting
language you already know.

## Registers (ch 20)

| | |
|---|---|
| `"ayy` `"ap` | yank into / paste from register a |
| `"Ayy` | append to register a |
| `"0p` | the last yank, unclobbered by deletes |
| `"_d` | black hole — delete without touching any register |
| `"+y` `"+p` | system clipboard |
| `"%` | current filename |
| `:reg` | show them all |
| `Ctrl-R a` | paste register a while in insert mode |

## Macros (ch 21)

```
qa ... q       record into register a
@a             play it
@@             play the last one again
10@a           play it ten times
:%normal @a    play it on every line
```

A macro is just keystrokes in a register, so `"ap` prints it and `"ayy`
puts an edited one back.

## Windows and buffers (ch 16)

| | |
|---|---|
| `:e file` | open |
| `:ls` `:b name` `:bn` `:bp` `:bd` | list / switch / next / previous / close |
| `:sp` `:vs` | split horizontally / vertically |
| `Ctrl-W h j k l` | move between windows |
| `Ctrl-W o` | only this window |
| `Ctrl-W =` | equalise sizes |
| `gf` | open the file under the cursor |

## Jumps and marks (ch 17)

| | |
|---|---|
| `Ctrl-O` `Ctrl-I` | back / forward through the jump list |
| `g;` `g,` | back / forward through *changes* |
| `ma` then `` `a `` | set mark a, jump to it |
| `` `. `` | where you last edited |
| `''` | where you were before the last jump |
| `Ctrl-6` | the previous buffer |

## Quickfix (ch 19)

```
:vimgrep /pattern/ **/*.ts     search the repo
:copen  :cn  :cp  :cc          list, next, previous, current
:cdo s/old/new/g | update      run a substitution on every hit
:cfdo %s/old/new/g | update    once per file instead of per line
```

## Ex commands (ch 24-25)

```
:10,20d        delete a range        :10,20m$      move to the end
:10,20t.       copy below here       :.,+5>        indent six lines
:%normal A;    run normal-mode keys on every line
:g/x/normal @q run a macro on matching lines
q:             the command-line window — edit your history like a buffer
```

Addresses: `.` here, `$` last line, `%` all, `'a` a mark, `/pat/` the next
match, `+3` `-3` relative.

## Talking to the shell (ch 26)

```
!ip!sort        filter a paragraph through sort
:%!jq .         pipe the whole file through jq
:r !date        read a command's output in
:w !sudo tee %  write a file you forgot to open as root
```

## Options worth knowing (ch 27)

```
:set number relativenumber
:set ignorecase smartcase
:set hlsearch incsearch
:set path=.,**          makes :find work like Ctrl+P
:set undofile           undo that survives closing the file
:verbose set shiftwidth?    which file set this, and where
```

## When it goes wrong

| | |
|---|---|
| stuck in something | `Esc` twice |
| stuck in a terminal or command window | `Ctrl-C`, then `Esc` |
| undid too far | `Ctrl-R` |
| file is a mess | `:e!` reloads from disk, losing your changes |
| want out, keep nothing | `:q!` |
| want out of everything | `:qa!` |
| swap file warning | someone (maybe a crashed vim) has it open; `R` recovers |
