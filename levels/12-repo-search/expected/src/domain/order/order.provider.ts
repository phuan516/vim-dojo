import { injectable, inject } from 'tsyringe';
import { exception } from '../../configuration/errors';
import { OrderRepository } from './order.repository';
import { StripeService } from '../../infrastructure/services/payment.service';

@injectable()
export class OrderProvider {
  constructor(
    @inject(OrderRepository) protected orderRepository: OrderRepository,
    @inject(StripeService) protected stripeService: StripeService,
  ) {}

  public async findOne(id: string) {
    const order = await this.orderRepository.findOne({ where: { id } });

    if (!order) {
      throw exception('ORDER_NOT_FOUND');
    }

    return order;
  }

  public async cancel(id: string) {
    const order = await this.findOne(id);

    if (order.status === 'SHIPPED') {
      throw exception('ORDER_ALREADY_SHIPPED');
    }

    await this.stripeService.refund(order.id);

    return this.orderRepository.update({
      where: { id },
      values: { status: 'CANCELLED' },
    });
  }
}
