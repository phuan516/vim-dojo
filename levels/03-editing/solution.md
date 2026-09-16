  /host   Enter     first host line
  j dd              down one, delete the duplicate

  /port   Enter
  o timeout: 5000,  Esc

  /databaseUrl Enter
  yy p              duplicate the line
  cw replicaUrl Esc rename the key on the copy

  /debgu  Enter
  ciw debug Esc     (or land on the g and press  xp  )

  :wq

  Notice you never selected anything. In vim you say what to do and
  what to do it to - the selection step disappears.
