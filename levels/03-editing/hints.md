Put the cursor anywhere on the duplicate line and press dd. Vim does
not care which column you are in - dd is a whole-line operation.
---
yy copies the line under the cursor. p pastes it on the line below.
So yyp duplicates a line in three keystrokes.
---
On the pasted copy, move to the word databaseUrl and press cw. The
word vanishes and you are in INSERT mode. Type replicaUrl, Esc.
---
'debgu' is two letters swapped. Land on the g and press  x  then  p .
x deletes the character AND copies it; p puts it back after the
cursor, which is exactly a transpose. Or: land on the word, ciw.
