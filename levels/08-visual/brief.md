  Visual mode is the one place vim works like every other editor:
  select first, then act. Use it when you cannot describe the target
  with a motion.

  The killer feature is VISUAL BLOCK ( Ctrl-V ): a rectangular
  selection down a column. It is how vim does the multi-cursor edits
  you use Alt+click for.

  In order.types.ts:

    1. Put  readonly  in front of all four field names - one edit,
       not four.
    2. Put a  ;  at the end of all four field lines - again one edit.
    3. Uppercase the three status strings: 'pending' -> 'PENDING' etc.

  Do steps 1 and 2 with Ctrl-V. Doing them four times by hand counts
  as failing the level even though the checker will pass you.
