  Vim has no clipboard shortcuts because it has something better:
  yank, delete and put. Deleting also copies, so "cut" and "copy"
  are the same idea with a different verb.

  In config.ts:

    1. One line is duplicated. Delete the second copy.
    2. Add  timeout: 5000,  directly under the port line.
    3. Copy the databaseUrl line, paste it underneath, and rename the
       key on the copy to  replicaUrl
    4. Fix the typo  'debgu'  ->  'debug'

  The point of step 3 is that you never touch the mouse and never
  retype the value.
