Do the two small ones first: the entity union and the JSON. Both are
"duplicate the neighbouring thing and edit the copy" - yyp, then ci'
or ci" on the copy.
---
For the provider: put the cursor on the "public async cancel" line,
press V then } to select down to the blank line before the closing
brace, then y. Press } to get past the block, then p.
---
Now edit the pasted copy. cancel -> archive is ciw. The === becomes
!== - land on it and use ce or ci( for the whole condition. The
SHIPPED error code becomes ORDER_NOT_CANCELLED - ci' on it.
Delete the refund line with dd, and the blank line it leaves.
---
The resolver method is short enough to copy cancelOrder with V}y }p
and change three words on the copy: cancelOrder -> archiveOrder and
cancel -> archive.
---
Check yourself at the end: :vimgrep /ARCHIVED/ **/* then :copen -
you should see the entity and the provider, and nothing unexpected.
