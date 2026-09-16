  /users     Enter
  ci" /api/v2/users/  Esc

  /if        Enter
  ci( result.status >= 400  Esc

  Put the cursor on  response  (on the const line):
  *           search for the word under the cursor, jumps to next one
  cgn result Esc     change this match
  .  .               repeat on the remaining two

  :wq

  Once verb+object is in your fingers you stop memorising commands.
  d2w, ci{, ya(, yt, - you can invent them because the grammar is
  regular.
