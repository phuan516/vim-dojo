import { injectable } from 'tsyringe';
import { Customer as CustomerRecord } from '@prisma/client';
import { BaseRepository } from '../../infrastructure/base.repository';
import { Customer } from './customer.entity';

@injectable()
export class CustomerRepository extends BaseRepository<CustomerRecord, Customer> {
  public toEntity(record: CustomerRecord): Customer {
    return {
      id: record.id,
      email: record.email,
      name: record.name,
    };
  }
}
