  v         visual: select characters
  V         visual line: select whole lines
  Ctrl-V    visual BLOCK: select a rectangle
  Esc       cancel the selection

  With a block selected:
    I  type  Esc     insert that text at the start of EVERY line
    A  type  Esc     append it to the end of every line
    $ then A         append at each line's own end, ragged edges fine
    d  /  c  /  y    delete / change / yank the rectangle
    r x              fill the whole block with x

  On any visual selection:
    U  /  u          upper case / lower case the selection
    >  /  <          indent / outdent      .  repeats it
    gv               reselect whatever you had selected last time
  Outside visual mode:
    gUiw             upper case the word under the cursor
