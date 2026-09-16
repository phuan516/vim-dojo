Put the cursor anywhere on the line with "/users/" and press ci"
The quotes stay, the contents vanish, you are in INSERT mode.
---
For the condition: put the cursor anywhere on the if line and press
ci( . Everything between the parentheses goes. Type the new
condition, Esc.
---
For the rename, the fast way: put the cursor on the word response
and press * to search for it. Then press cgn , type result , Esc.
Now press n . n . to find and change the rest. Or simply hold . -
cgn re-runs the search itself.
---
The slow-but-fine way: ciw result Esc on the first one, then n to
jump to the next match and . to repeat the change.
