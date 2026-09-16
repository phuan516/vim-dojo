  Ctrl+Shift+F gives you a list of matches across the project and you
  click each one. Vim's version is the QUICKFIX LIST: a search fills
  it, :cn walks it, and the file each result lives in opens as you go.

      :vimgrep /PaymentService/ **/*.ts
      :copen        see the list
      :cn  :cp      next / previous result

  The payments integration moved to Stripe. Rename the class
  PaymentService to StripeService everywhere in src/ - the class
  itself, both import lines, the injected property, the constructor
  type, and the DI registration.

  The injected property is called paymentService. Framework rule: an
  injected dependency is named after its class, so it becomes
  stripeService. Rename its uses too.

  Do NOT rename the file. Do NOT touch anything in the errors JSON.
