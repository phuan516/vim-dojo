:ls shows you what is loaded. The % marks the buffer you are looking
at, the # marks the one Ctrl-^ will flip you to.
---
:vs then Ctrl-W l puts you in the right-hand split. Then :b default
switches that split to the JSON file - the split shows a different
buffer from the left one.
---
In the JSON, put the cursor on the ORDER_ALREADY_SHIPPED line and
press yy p to duplicate it, then edit the copy. Same trick as level 3
and it keeps the formatting identical for free.
---
In the provider, the whole SHIPPED guard is four lines. V3j y is
"select this line and three more, yank". Then p, then fix the two
words on the copy.
