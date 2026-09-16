  This is the thing vim has that your editor does not.

  A macro is a recording of your keystrokes, saved into a register,
  replayable any number of times. Not a script - literally the keys
  you pressed, played back.

  Turn the eight bare words in status.labels.ts into object entries:

      pending        ->      PENDING: 'pending',

  Record the transformation on the FIRST line, ending with j so the
  cursor lands ready on the next one. Then replay it seven times with
  7@a .  (or @a to test one line first, then 6@a)

  If your recording goes wrong, do not repair it - press q, undo, and
  record it again. Re-recording is cheap. That is the whole skill.
