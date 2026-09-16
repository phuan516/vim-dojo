  :s/old/new/          replace the FIRST match on this line
  :s/old/new/g         every match on this line
  :%s/old/new/g        every match in the whole file    ( % = all lines )
  :%s/old/new/gc       ...and ask me about each one  (y n a q l)
  :10,20s/old/new/g    only lines 10 to 20
  :'<,'>s/old/new/g    only the lines I just visually selected
  :%s/\<old\>/new/g    whole word only - not "oldest", not "goldold"
  :%s/old/new/gi       ignore case when matching
  &                    repeat the last :s on this line
  u                    undo the whole substitution in one go
