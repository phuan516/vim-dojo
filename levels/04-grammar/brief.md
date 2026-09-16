  This is the level where vim stops being a weird editor and starts
  being a language.

  Commands are  verb + object .  d is delete, c is change, y is yank.
  The object can be a motion (dw = delete word) or a TEXT OBJECT:

      iw  inner word        i"  inside the quotes
      i(  inside the parens i{  inside the braces
      it  inside the tag

  ci"  means "change inside the quotes" and it works from anywhere on
  the line. You do not have to be inside the quotes already.

  In user.service.ts:

    1. "/users/"  ->  "/api/v2/users/"      without retyping the quotes
    2. the whole if condition  ->  result.status >= 400
    3. rename all three  response  ->  result

  Step 3 is VS Code's Ctrl+D multi-cursor. Vim does it with  .  , the
  repeat command: do the edit once, then press . on each other one.
