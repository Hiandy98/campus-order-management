const BASE = '/api/v1'

export interface Stock {
  name: string
  stock: number
  soldout: boolean
  price?: number
}

export interface OrderItem {
  name: string
  qty: number
}

export interface Order {
  id: number
  pickup_no: number | string
  items_summary: string
  status: 'pending' | 'ready' | 'completed' | 'cancelled'
  created_at: string
  ready_at?: string | null
  cancel_reason?: string | null
}

export type CancelReason = '客人跑了' | '餐點做錯' | '食材沒了' | '其他'

async function req<T = unknown>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({} as any))
    throw new Error(err?.detail || `系統錯誤 (${res.status})`)
  }

  if (res.status === 204) return undefined as T

  const text = await res.text()
  return (text ? JSON.parse(text) : undefined) as T
}

export const api = {
  getStocks: () => req<Stock[]>('/stocks'),
  updateStock: (name: string, patch: Partial<Pick<Stock, 'stock' | 'soldout'>>) =>
    req(`/stocks/${encodeURIComponent(name)}`, {
      method: 'PATCH',
      body: JSON.stringify(patch),
    }),

  createOrder: (items: OrderItem[]) =>
    req<Order>('/orders', {
      method: 'POST',
      body: JSON.stringify({ items }),
    }),

  listOrders: (status: Order['status']) => req<Order[]>(`/orders?status=${status}`),

  updateStatus: (id: number, body: { status: Order['status']; cancel_reason?: CancelReason }) =>
    req(`/orders/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify(body),
    }),
}