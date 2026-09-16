Get to line 2, column 0, before you press qa. Where you start
recording is where every replay assumes it starts.
---
One recipe that works:
  ^  yiw            go to the word, copy it
  A: '  Esc         append  : '  at the end of the line
  p                 paste the word inside the quotes
  A',  Esc          close the quote and add the comma
  ^ gUiw            upper case the key at the front
  I<space><space> Esc   indent by two
  j                 land on the next line - this is what makes it repeat
---
Now press q to stop, then @a once and watch a single line transform.
If it worked, 6@a does the six after it.
---
Went wrong? u until the file is back, then qa and record again. Do
not try to patch a broken macro on your first day.
