  :%s/Basket/Cart/g          the class name
  :%s/basket/cart/gc         then: y y y n y y y y y  (n on the string)
  :wq

  Reading a substitute command out loud helps:
  " : (over) % all lines  s substitute  / basket / for cart /
    g every one on the line, c and ask me first "

  The pattern half of :s is a regex, so \d, \s, \(groups\) and \1
  backreferences all work. :h pattern when you need them.
