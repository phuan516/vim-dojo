import { Resolver, Query } from '../types';

export class BasketResolver {
  public async basket(_: unknown, args: { basketId: string }) {
    const basket = await this.basketProvider.findOne(args.basketId);

    if (!basket) {
      return { error: 'Your basket is empty' };
    }

    return {
      id: basket.id,
      items: basket.items,
      total: basket.total,
    };
  }
}
