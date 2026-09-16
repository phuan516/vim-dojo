  Ctrl+P is probably the shortcut you press most in VS Code. Plain vim
  has :find, and it is genuinely good once you tell it to look in
  subdirectories:

      :set path=.,**

  Now  :find customer.entity.ts  opens that file from anywhere in the
  tree, and Tab completes partial names. Put that one setting in your
  vimrc tonight and you have 80% of Ctrl+P.

  Answer the four questions in answers.txt. Each one lives in a
  different file. Open each by name.

  Get back to answers.txt each time with Ctrl-^ - it flips between
  the current file and the previous one, which is exactly this job.
