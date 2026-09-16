  :set number
  :%s/customerId//gn     -> the count
  :%s/records//gn        -> the count
  gg /toEntity Enter     -> first match, read the line number
  G  ?deleted Enter      -> last match, read the line number

  :bn  fill in answers.txt  :wa

  The habit: * is free. Cursor on a symbol, press *, you are at the
  next use of it. It replaces "select the word, Ctrl+F, Enter".
