export type Order = {
  id: string;
  customerId: string;
  status: OrderStatus;
  total: number;
  cancellationReason?: string;
};

export type OrderStatus = 'PENDING' | 'SHIPPED' | 'CANCELLED' | 'ARCHIVED';
