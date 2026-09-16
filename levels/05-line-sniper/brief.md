  w and b move by word, which is often too coarse. To land on an exact
  character, use f (find). fx puts the cursor on the next x on this
  line. It is the single biggest speed-up available on a long line.

  f and t combine with operators, so  dt"  means "delete up to the
  next quote" and  ct,  means "change up to the next comma".

  In query.ts:

    1. "PENDING"  ->  "SHIPPED"
    2. limit: 50  ->  limit: 25
    3. delete the  phone,  field from the csv string
    4. "Order #1042 - awaiting payment - do not ship"
         ->  "Order #1042 - ready to ship"

  No arrow keys. Aim with f.
