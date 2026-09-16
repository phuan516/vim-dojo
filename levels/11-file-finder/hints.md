Run :set path=.,** first. Without it, :find only looks in the
current directory and will tell you the file does not exist.
---
:find custom then press Tab. Vim fills in the rest. If several files
match, press Tab again to cycle and Enter to pick.
---
Ctrl-^ is the fastest way back to answers.txt. It means "the other
file", and after you have opened something it always points home.
---
For the register count, open registry.ts and run
  :%s/container.register//gn   - it counts without changing anything.
