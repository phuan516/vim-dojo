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
