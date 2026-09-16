import { injectable } from 'tsyringe';
import { Order as OrderRecord } from '@prisma/client';
import { BaseRepository } from '../../infrastructure/base.repository';
import { Order } from './order.entity';

@injectable()
export class OrderRepository extends BaseRepository<OrderRecord, Order> {
  public async findByCustomer(args: { customerId: string }) {
    const records = await this.prisma.order.findMany({
      where: { customerId: args.customerId, deleted: null },
    });

    return records.map((record) => this.toEntity(record));
  }

  public toEntity(record: OrderRecord): Order {
    return {
      id: record.id,
      customerId: record.customerId,
      status: record.status,
      total: record.total,
      cancellationReason: record.cancellationReason ?? undefined,
    };
  }
}
