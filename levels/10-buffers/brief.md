  VS Code has tabs. Vim has BUFFERS: every file you open stays loaded,
  whether or not it is on screen. Windows (splits) are just viewports
  onto buffers. The two ideas are separate, which is why closing a
  split does not close the file.

  Two files are already open as buffers. Make this change across both:

    1. In default.json, add an error code, keeping the file valid JSON
       and the same formatting as its neighbours:
         "ORDER_ALREADY_CANCELLED": { "statusCode": 409, "sentry": false }
       Put it directly after the ORDER_ALREADY_SHIPPED line.

    2. In order.provider.ts, in cancel(), add a second guard directly
       below the SHIPPED one:

         if (order.status === 'CANCELLED') {
           throw exception('ORDER_ALREADY_CANCELLED');
         }

       with a blank line between the two guards, matching the file's
       existing spacing.

  Do it with the two files in a vertical split so you can see both.
