import { Resolver, Query } from '../types';

export class CartResolver {
  public async cart(_: unknown, args: { cartId: string }) {
    const cart = await this.cartProvider.findOne(args.cartId);

    if (!cart) {
      return { error: 'Your basket is empty' };
    }

    return {
      id: cart.id,
      items: cart.items,
      total: cart.total,
    };
  }
}
