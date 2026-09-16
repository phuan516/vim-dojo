  :set path=.,**       look in every subdirectory  (put this in .vimrc)
  :find name.ts        open a file by name from anywhere in the tree
  :find cust<Tab>      Tab completes; Tab again cycles the candidates
  :b cust              switch to an already-open buffer by partial name
  Ctrl-^               flip between this file and the last one
  :Ex   or  :e .       open vim's built-in file browser on a directory
  :Sex  :Vex           that browser in a horizontal / vertical split
  gf                   open the file named under the cursor
  :set wildmenu        show completions as a menu (already in your vimrc)

  Later, when you want real fuzzy matching, the plugin everyone uses
  is fzf.vim - but learn :find first so you know what it is doing.
