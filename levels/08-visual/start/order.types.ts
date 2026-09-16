type Order = {
  id: string
  customerId: string
  status: string
  total: number
}

const statuses = [
  'pending',
  'shipped',
  'cancelled',
]
