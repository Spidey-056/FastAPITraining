// src/pages/OrdersPage.jsx
// Lists all orders and allows creating a new order.
// Supports deleting orders and viewing order details (items, payment & delivery status).
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getOrders, createOrder, deleteOrder, getUsers } from '../api/client'

const PAYMENT_STATUSES = ['pending', 'paid', 'failed', 'refunded']
const DELIVERY_STATUSES = ['pending', 'shipped', 'in_transit', 'delivered', 'returned', 'cancelled']

const PAYMENT_BADGES = {
  pending: 'warning text-dark',
  paid: 'success',
  failed: 'danger',
  refunded: 'info text-dark',
}

const DELIVERY_BADGES = {
  pending: 'secondary',
  shipped: 'primary',
  in_transit: 'info text-dark',
  delivered: 'success',
  returned: 'warning text-dark',
  cancelled: 'dark',
}

const blankForm = {
  order_number: '',
  customer_id: '',
  itemName: '',
  itemQuantity: 1,
  itemPrice: 0,
  payment_status: 'paid',
  delivery_status: 'delivered',
}

export default function OrdersPage() {
  const [orders, setOrders] = useState([])
  const [users, setUsers] = useState([])
  const [form, setForm] = useState(blankForm)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    getOrders().then(setOrders).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
    getUsers().then(setUsers).catch(() => {})
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    const qty = parseInt(form.itemQuantity, 10) || 1
    const unitPrice = parseFloat(form.itemPrice) || 0
    const totalAmount = qty * unitPrice

    const payload = {
      order_number: form.order_number.trim(),
      customer_id: form.customer_id,
      items: form.itemName ? [{ name: form.itemName, quantity: qty, price: unitPrice }] : [],
      total_amount: totalAmount,
      payment_status: form.payment_status,
      delivery_status: form.delivery_status,
    }

    try {
      await createOrder(payload)
      setForm(blankForm)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this order?')) return
    try {
      await deleteOrder(id)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <h4>Customer Orders</h4>
      <p className="text-muted small">
        Orders placed by customers. Support tickets can be linked to these orders to assist support agents during investigation.
      </p>

      {/* Create Order Form */}
      <form onSubmit={handleSubmit} className="card p-3 mb-4 bg-light">
        <h6 className="card-subtitle mb-2 fw-bold">Create New Order</h6>
        <div className="row g-2">
          <div className="col-md-3">
            <input
              className="form-control form-control-sm"
              placeholder="Order Number (e.g. ORD-1001)"
              required
              value={form.order_number}
              onChange={(e) => setForm({ ...form, order_number: e.target.value })}
            />
          </div>
          <div className="col-md-3">
            <select
              className="form-select form-select-sm"
              required
              value={form.customer_id}
              onChange={(e) => setForm({ ...form, customer_id: e.target.value })}
            >
              <option value="">-- Customer --</option>
              {users.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.name} ({u.role})
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-3">
            <input
              className="form-control form-control-sm"
              placeholder="Item Name (e.g. Mechanical Keyboard)"
              required
              value={form.itemName}
              onChange={(e) => setForm({ ...form, itemName: e.target.value })}
            />
          </div>
          <div className="col-md-1">
            <input
              type="number"
              className="form-control form-control-sm"
              placeholder="Qty"
              min={1}
              required
              value={form.itemQuantity}
              onChange={(e) => setForm({ ...form, itemQuantity: e.target.value })}
            />
          </div>
          <div className="col-md-2">
            <input
              type="number"
              step="0.01"
              className="form-control form-control-sm"
              placeholder="Price (₹)"
              min={0}
              required
              value={form.itemPrice}
              onChange={(e) => setForm({ ...form, itemPrice: e.target.value })}
            />
          </div>

          <div className="col-md-3">
            <label className="form-label small text-muted mb-0">Payment Status</label>
            <select
              className="form-select form-select-sm"
              value={form.payment_status}
              onChange={(e) => setForm({ ...form, payment_status: e.target.value })}
            >
              {PAYMENT_STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s.toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          <div className="col-md-3">
            <label className="form-label small text-muted mb-0">Delivery Status</label>
            <select
              className="form-select form-select-sm"
              value={form.delivery_status}
              onChange={(e) => setForm({ ...form, delivery_status: e.target.value })}
            >
              {DELIVERY_STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s.toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          <div className="col-md-3 d-flex align-items-end">
            <button className="btn btn-sm btn-primary w-100" type="submit">
              Save Order
            </button>
          </div>
          {error && <div className="col-12"><small className="text-danger">{error}</small></div>}
        </div>
      </form>

      {/* Orders Table */}
      {loading ? (
        <p>Loading…</p>
      ) : (
        <table className="table table-sm table-bordered table-hover align-middle">
          <thead className="table-dark">
            <tr>
              <th>Order #</th>
              <th>Customer</th>
              <th>Items</th>
              <th>Total Amount</th>
              <th>Payment</th>
              <th>Delivery</th>
              <th>Placed On</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {orders.length === 0 && (
              <tr>
                <td colSpan={8} className="text-center text-muted">
                  No orders yet.
                </td>
              </tr>
            )}
            {orders.map((o) => (
              <tr key={o.id}>
                <td className="fw-semibold">{o.order_number}</td>
                <td>{users.find((u) => u.id === o.customer_id)?.name || o.customer_id}</td>
                <td>
                  {o.items?.length > 0
                    ? o.items.map((it, idx) => (
                        <div key={idx} className="small">
                          {it.name} (x{it.quantity}) - ₹{it.price}
                        </div>
                      ))
                    : <span className="text-muted small">No items</span>}
                </td>
                <td>₹{Number(o.total_amount).toFixed(2)}</td>
                <td>
                  <span className={`badge bg-₹{PAYMENT_BADGES[o.payment_status] || 'secondary'}`}>
                    {o.payment_status}
                  </span>
                </td>
                <td>
                  <span className={`badge bg-₹{DELIVERY_BADGES[o.delivery_status] || 'secondary'}`}>
                    {o.delivery_status}
                  </span>
                </td>
                <td>{new Date(o.created_at).toLocaleDateString()}</td>
                <td>
                  <button
                    className="btn btn-sm btn-outline-danger"
                    onClick={() => handleDelete(o.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
