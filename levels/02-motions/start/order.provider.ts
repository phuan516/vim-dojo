import { injectable, inject } from 'tsyringe';
import { OrderRepository } from '../repositories/order.repository';
import { PaymentService } from '../services/payment.service';
import { exception } from '../exceptions';

@injectable()
export class OrderProvider {
  constructor(
    @inject(OrderRepository) protected orderRepository: OrderRepository,
    @inject(PaymentService) protected paymentService: PaymentService,
  ) {}

  public async findOne(id: string) {
    const order = await this.orderRepository.findOne({ where: { id } });

    if (!order) {
      throw exception('ORDER_NOT_FOUND');
    }

    return order;
  }

  public async cancel(id: string, reason: string) {
    const order = await this.findOne(id);

    if (order.status === 'SHIPPED') {
      throw exception('ORDER_ALREADY_SHIPPED');
    }

    await this.paymentService.refund(order.paymentId);

    return this.orderRepository.update({
      where: { id },
      values: { status: 'CANCELLED', cancellationReason: reason },
    });
  }
}
