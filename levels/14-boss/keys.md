  Everything so far. The moves that matter here:

  :find order.entity.ts    open by name        Ctrl-^  flip back
  V }  y                   select a whole block of lines and yank it
  }p                       paste it after the next blank line
  ci( ci" ciw              change inside brackets / quotes / word
  *  then  cgn  then  .    rename a symbol through a file
  :%s/old/new/gc           rename with confirmation
  Ctrl-O                   get back to where you just were
  :wa  :qa                 save everything, quit everything
