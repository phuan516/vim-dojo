import { injectable, inject } from 'tsyringe';
import { exception } from '../../configuration/errors';
import { CustomerRepository } from './customer.repository';

@injectable()
export class CustomerProvider {
  constructor(
    @inject(CustomerRepository) protected customerRepository: CustomerRepository,
  ) {}

  public async findOne(id: string) {
    const customer = await this.customerRepository.findOne({ where: { id } });

    if (!customer) {
      throw exception('CUSTOMER_NOT_FOUND');
    }

    return customer;
  }
}
