import { injectable } from 'tsyringe';
import { exception } from '../../configuration/errors';

@injectable()
export class PaymentService {
  public async refund(orderId: string) {
    const response = await this.http.post(`/refunds`, { orderId });

    if (response.status !== 200) {
      throw exception('REFUND_FAILED');
    }

    return response.data;
  }
}
