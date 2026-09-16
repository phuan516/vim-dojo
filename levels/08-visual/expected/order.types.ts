type Order = {
  readonly id: string;
  readonly customerId: string;
  readonly status: string;
  readonly total: number;
}

const statuses = [
  'PENDING',
  'SHIPPED',
  'CANCELLED',
]
