import { container } from 'tsyringe';
import { OrderRepository } from '../domain/order/order.repository';
import { OrderProvider } from '../domain/order/order.provider';
import { OrderResolver } from '../domain/order/order.resolver';
import { CustomerRepository } from '../domain/customer/customer.repository';
import { CustomerProvider } from '../domain/customer/customer.provider';
import { PaymentService } from '../infrastructure/services/payment.service';
import { EmailService } from '../infrastructure/services/email.service';

container.register('OrderRepository', { useClass: OrderRepository });
container.register('CustomerRepository', { useClass: CustomerRepository });
container.register('OrderProvider', { useClass: OrderProvider });
container.register('CustomerProvider', { useClass: CustomerProvider });
container.register('PaymentService', { useClass: PaymentService });
container.register('EmailService', { useClass: EmailService });
container.register('OrderResolver', { useClass: OrderResolver });
