import { injectable } from 'tsyringe';
import { Order as OrderRecord, PrismaClient } from '@prisma/client';
import { BaseRepository } from './base.repository';
import { Order } from '../entities/order.entity';

@injectable()
export class OrderRepository extends BaseRepository<OrderRecord, Order> {
  public async findByCustomer(customerId: string) {
    const records = await this.prisma.order.findMany({
      where: { customerId, deleted: null },
      orderBy: { created: 'desc' },
    });

    return records.map((record) => this.toEntity(record));
  }

  public async findPending(customerId: string) {
    const records = await this.prisma.order.findMany({
      where: { customerId, status: 'PENDING', deleted: null },
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
