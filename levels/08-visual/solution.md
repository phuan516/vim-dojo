  2G ^                      first field name
  Ctrl-V jjj                block down four lines
  I readonly<space> Esc     appears on all four

  2G Ctrl-V jjj $ A ; Esc   semicolon on every line end

  /pending Enter
  gUiw                      'PENDING'
  j .    j .                repeat on the other two

  :wq

  Rule of thumb: if you are about to do the same small edit on
  several consecutive lines, that is Ctrl-V. If the lines are
  scattered, that is  *  and  .  from level 4.
