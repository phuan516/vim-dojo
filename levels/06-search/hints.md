:%s/customerId//gn prints "N matches on N lines" at the bottom and
changes nothing. The gn flag is the trick - g means every match on
each line, n means "just count".
---
Beware: /records also matches "record" inside other words? No - but
it does match "records" inside nothing else here. Whole-word search
is  /\<records\>  , and * does that for you automatically.
---
For line numbers, turn on :set number , then /toEntity and read the
line you land on. Press n to walk to the later matches.
---
?deleted searches BACKWARDS from the cursor. Press G first to get to
the bottom, then ?deleted finds the last one directly.
