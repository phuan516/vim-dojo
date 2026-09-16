  No new keys. This is a real ticket, done entirely in vim.

  TICKET: a cancelled order can be archived so it drops out of the
  customer's order list.

  1. src/domain/order/order.entity.ts
     Add 'ARCHIVED' to the OrderStatus union, last, same style.

  2. src/configuration/errors/default.json
     Add, directly after the ORDER_ALREADY_SHIPPED line:
       "ORDER_NOT_CANCELLED": { "statusCode": 409, "sentry": false },

  3. src/domain/order/order.provider.ts
     Add an archive method directly below cancel(), separated by one
     blank line, exactly:

  public async archive(id: string) {
    const order = await this.findOne(id);

    if (order.status !== 'CANCELLED') {
      throw exception('ORDER_NOT_CANCELLED');
    }

    return this.orderRepository.update({
      where: { id },
      values: { status: 'ARCHIVED' },
    });
  }

     (indented two spaces, as a class member.)

  4. src/domain/order/order.resolver.ts
     Add below cancelOrder, separated by one blank line:

  public async archiveOrder(_: unknown, args: { id: string }) {
    return this.orderProvider.archive(args.id);
  }

  Par is 700 keystrokes. Typing all of that out by hand is about 900.
  Getting under par means copying the cancel method and editing it,
  not retyping it.
