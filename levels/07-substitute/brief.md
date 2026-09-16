  The product is being renamed from "basket" to "cart".

  Rename every identifier in cart.resolver.ts:
    basket -> cart      basketId -> cartId
    basketProvider -> cartProvider     BasketResolver -> CartResolver

  EXCEPT the message shown to the customer:
    'Your basket is empty'    must stay exactly as it is.

  That exception is the whole lesson. A blind replace-all breaks it.
  You have two honest ways out: replace with confirmation and skip
  that one, or write a pattern precise enough not to match it.

  Notice also that replacing "basket" does not touch "Basket" -
  substitution is case sensitive unless you say otherwise.
