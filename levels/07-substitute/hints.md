Start with  :%s/basket/cart/gc  - the c means confirm. Vim highlights
each match and waits. Press y to replace, n to skip, a to do all the
rest, q to stop. Skip the one inside the quotes.
---
Capital B is a separate job:  :%s/Basket/Cart/g
---
If you replaced the string by accident, u undoes the ENTIRE
substitution in one press, not one match at a time.
---
The pattern-precision route instead of confirming: the bad match is
the only one followed by a space and the word "is". Everything you
DO want is followed by a letter, a dot, an ampersand or a bracket.
For example  :%s/basket\([A-Z.,)( ]\)\@=/cart/g  works, but honestly
gc is the tool a working engineer reaches for. Precision patterns are
for when there are two hundred matches, not eleven.
