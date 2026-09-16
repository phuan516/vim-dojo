  :set path=.,**

  :find customer.entity.ts        count the fields    Ctrl-^
  :find default.json              find "sentry": true  Ctrl-^
  :find base.repository.ts        read the class name  Ctrl-^
  :find registry.ts
  :%s/container.register//gn      the count            Ctrl-^

  fill in answers.txt, :wa

  Tonight, in ~/.vimrc:
      set path=.,**
      set wildmenu
      set wildmode=longest:full,full
  Those three lines are your Ctrl+P.
