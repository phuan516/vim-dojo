  :e path/to/file    open a file into a new buffer
  :ls               list the buffers, each with a number
  :b 3              switch to buffer 3
  :b order.prov     switch by partial name - no number needed
  :bn  :bp          next / previous buffer
  Ctrl-^            flip to the previous buffer - the one you use most
  :bd               close this buffer (the file, not the window)

  :vs path          open a file in a VERTICAL split
  :sp path          horizontal split
  Ctrl-W  then h j k l    move between splits
  Ctrl-W  then =          make the splits equal size
  Ctrl-W  then o          close every split but this one
  Ctrl-W  then q          close this split

  :w    save this file       :wa   save every changed file
  :qa   quit everything      :wqa  save everything and quit
