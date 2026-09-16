  :vimgrep /PaymentService/ **/*.ts
  :cdo s/PaymentService/StripeService/g | update

  :vimgrep /paymentService/ **/*.ts
  :cdo s/paymentService/stripeService/g | update

  :vimgrep /[Pp]aymentService/ **/*.ts     should report "no match"
  :qa

  The manual version is worth doing once so you believe it:
  :copen , then :cn / edit / :cn ... all the way down the list.

  :cdo is the single command that replaces the whole Ctrl+Shift+F
  "replace all in files" panel, and unlike that panel you can put any
  vim command after it, not just a substitution.
