import { injectable, inject } from 'tsyringe';
import { OrderProvider } from './order.provider';

@injectable()
export class OrderResolver {
  constructor(@inject(OrderProvider) protected orderProvider: OrderProvider) {}

  public async order(_: unknown, args: { id: string }) {
    return this.orderProvider.findOne(args.id);
  }

  public async cancelOrder(_: unknown, args: { id: string }) {
    return this.orderProvider.cancel(args.id);
  }
}
