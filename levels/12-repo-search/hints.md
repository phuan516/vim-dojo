Start with :vimgrep /PaymentService/ **/*.ts then :copen to see how
many places you have to touch. Count them before you start.
---
:cn moves to the next match and opens its file for you. You do not
need to open anything by hand.
---
The one-command version, once you trust it:
  :vimgrep /PaymentService/ **/*.ts
  :cdo s/PaymentService/StripeService/g | update
"update" writes the file only if it changed. Then repeat the pair for
paymentService -> stripeService.
---
Careful with ordering: replacing paymentService first would also hit
the capital-P class name? No - :s is case sensitive, so the two
renames are independent. But do check the result with a fresh
:vimgrep /[Pp]aymentService/ **/*.ts - it should come back empty.
