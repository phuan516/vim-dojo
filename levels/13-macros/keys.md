  qa        start recording into register a  ( "recording @a" appears )
  q         stop recording
  @a        play the macro back once
  7@a       play it seven times
  @@        play the LAST macro again

  Making a macro repeatable:
    - start from a predictable place on the line  ( ^ or 0 )
    - finish by moving to the next line  ( j )
    - never use arrow keys or counts that depend on where you are

  Useful in this level:
    yiw       yank the word under the cursor
    gUiw      upper case the word under the cursor
    A  I      append at end of line / insert at start of line
    p         put the yanked word back

  See what you recorded:   :reg a
  Fix a bad macro by hand: put the cursor on a blank line, "ap to
  paste it as text, edit it, then "ay$ to yank it back into a.
