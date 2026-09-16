  :set path=.,**

  ENTITY     :find order.entity.ts
             /OrderStatus Enter  f'  ...  A | 'ARCHIVED'; Esc
             (or yank the last member and edit the copy)

  JSON       :find default.json
             /ALREADY_SHIPPED Enter  yy p  ci" ORDER_NOT_CANCELLED Esc
             then fix the statusCode/sentry on the copy if needed

  PROVIDER   :find order.provider.ts
             /public async cancel Enter
             V } y            yank the whole method
             } p              paste it below
             on the copy:
               /archive... no - ciw archive   on the method name
               f= ci( order.status !== 'CANCELLED' Esc
               /ALREADY_SHIPPED Enter  ci' ORDER_NOT_CANCELLED Esc
               /refund Enter  dd  dd      drop the refund + blank line
               /CANCELLED' Enter (in values) ci' ARCHIVED Esc

  RESOLVER   :find order.resolver.ts
             /cancelOrder Enter  V } y  } p
             on the copy: ciw archiveOrder , then /cancel Enter ciw archive

  :wa :qa

  If you got through this without touching the mouse, you are past
  the hump. Everything after this is vocabulary, not concepts.
