# app/seed_data.py
#
# Purpose:
#   Seeds MongoDB with sample data tailored for the E-Commerce Customer Support System:
#   - Users (customers, support agents, team lead, admin)
#   - Categories (Order Not Received, Wrong Item, Damaged, Cancel, Refund, Return, etc.)
#   - Orders (customer orders with items, amounts, payment and delivery statuses)
#   - Tickets (linked to orders with lifecycles and assignments)
#   - Comments (ticket conversations between customers and agents)
#   - Attachments (metadata for photo proofs and receipts)
#   - Audit Logs (historical audit trail)

from datetime import datetime, timedelta
from app.database import database


def days_ago(d: int, hours: int = 0) -> datetime:
    """Helper returning a UTC datetime d days and hours ago."""
    return datetime.utcnow() - timedelta(days=d, hours=hours)


# --- 1. Users -----------------------------------------------------------------
USERS = [
    {
        "id": "user-cust-1",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "password": "Password123!",
        "role": "customer",
        "created_at": days_ago(30),
    },
    {
        "id": "user-cust-2",
        "name": "Bob Smith",
        "email": "bob@example.com",
        "password": "Password123!",
        "role": "customer",
        "created_at": days_ago(25),
    },
    {
        "id": "user-cust-3",
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "password": "Password123!",
        "role": "customer",
        "created_at": days_ago(20),
    },
    {
        "id": "user-agent-1",
        "name": "David Miller",
        "email": "david@support.com",
        "password": "Password123!",
        "role": "support_agent",
        "created_at": days_ago(60),
    },
    {
        "id": "user-agent-2",
        "name": "Emma Watson",
        "email": "emma@support.com",
        "password": "Password123!",
        "role": "support_agent",
        "created_at": days_ago(60),
    },
    {
        "id": "user-lead-1",
        "name": "Frank Castle",
        "email": "frank@support.com",
        "password": "Password123!",
        "role": "support_team_lead",
        "created_at": days_ago(90),
    },
    {
        "id": "user-admin-1",
        "name": "Grace Hopper",
        "email": "grace@ecom.com",
        "password": "Password123!",
        "role": "admin",
        "created_at": days_ago(120),
    },
]

# --- 2. Categories ------------------------------------------------------------
CATEGORIES = [
    {
        "id": "cat-order-not-rec",
        "name": "Order Not Received",
        "description": "Shipment marked delivered or past expected ETA but customer has not received it.",
        "created_at": days_ago(40),
    },
    {
        "id": "cat-wrong-item",
        "name": "Wrong Item Received",
        "description": "Received different product, variant, color, or model than what was ordered.",
        "created_at": days_ago(40),
    },
    {
        "id": "cat-damaged-item",
        "name": "Damaged Item",
        "description": "Item or packaging arrived broken, defective, or physically damaged.",
        "created_at": days_ago(40),
    },
    {
        "id": "cat-cancel-order",
        "name": "Cancel Order",
        "description": "Request to cancel an order prior to warehouse packaging and courier dispatch.",
        "created_at": days_ago(40),
    },
    {
        "id": "cat-refund",
        "name": "Refund Request",
        "description": "Queries regarding refund status, processing timeline, or billing reimbursement.",
        "created_at": days_ago(40),
    },
    {
        "id": "cat-return",
        "name": "Return & Exchange",
        "description": "Return merchandise authorization (RMA), drop-off labels, and product replacements.",
        "created_at": days_ago(40),
    },
    {
        "id": "cat-payment-issue",
        "name": "Payment Issue",
        "description": "Double charges, failed checkout transactions, or gift card/promo code issues.",
        "created_at": days_ago(40),
    },
    {
        "id": "cat-delivery-issue",
        "name": "Delivery Issue",
        "description": "Courier delays, incorrect shipping address, or delivery rescheduling requests.",
        "created_at": days_ago(40),
    },
]

# --- 3. Orders ----------------------------------------------------------------
ORDERS = [
    {
        "id": "order-1",
        "order_number": "ORD-90210",
        "customer_id": "user-cust-1",
        "items": [
            {"name": "Sony WH-1000XM5 Wireless Headphones (Black)", "quantity": 1, "price": 399.99},
            {"name": "Braided USB-C Fast Charger Cable", "quantity": 1, "price": 19.99},
        ],
        "total_amount": 419.98,
        "payment_status": "paid",
        "delivery_status": "delivered",
        "created_at": days_ago(7),
        "updated_at": days_ago(4),
    },
    {
        "id": "order-2",
        "order_number": "ORD-90211",
        "customer_id": "user-cust-2",
        "items": [
            {"name": "Mechanical Gaming Keyboard RGB (Tactile Switches)", "quantity": 1, "price": 129.99},
        ],
        "total_amount": 129.99,
        "payment_status": "paid",
        "delivery_status": "delivered",
        "created_at": days_ago(5),
        "updated_at": days_ago(2),
    },
    {
        "id": "order-3",
        "order_number": "ORD-90212",
        "customer_id": "user-cust-3",
        "items": [
            {"name": "27-inch 4K IPS Gaming Monitor 144Hz", "quantity": 1, "price": 349.50},
            {"name": "HDMI 2.1 Ultra High Speed Cable 2m", "quantity": 2, "price": 14.99},
        ],
        "total_amount": 379.48,
        "payment_status": "paid",
        "delivery_status": "in_transit",
        "created_at": days_ago(4),
        "updated_at": days_ago(1),
    },
    {
        "id": "order-4",
        "order_number": "ORD-90213",
        "customer_id": "user-cust-1",
        "items": [
            {"name": "Smart Fitness Watch Series 7", "quantity": 1, "price": 219.00},
        ],
        "total_amount": 219.00,
        "payment_status": "pending",
        "delivery_status": "pending",
        "created_at": days_ago(2),
        "updated_at": days_ago(2),
    },
    {
        "id": "order-5",
        "order_number": "ORD-90214",
        "customer_id": "user-cust-2",
        "items": [
            {"name": "Ergonomic Mesh Office Chair with Lumbar Support", "quantity": 1, "price": 185.00},
        ],
        "total_amount": 185.00,
        "payment_status": "refunded",
        "delivery_status": "returned",
        "created_at": days_ago(14),
        "updated_at": days_ago(2),
    },
]

# --- 4. Tickets (Linked to Orders) -------------------------------------------
TICKETS = [
    {
        "id": "ticket-1",
        "title": "Received Silver model instead of Black Headphones",
        "description": "I ordered the Black Sony headphones under order ORD-90210, but opened the box to find the Silver version. Please exchange for Black.",
        "category_id": "cat-wrong-item",
        "order_id": "order-1",
        "status": "in_progress",
        "created_by": "user-cust-1",
        "assigned_to": "user-agent-1",
        "created_at": days_ago(4),
        "updated_at": days_ago(2),
    },
    {
        "id": "ticket-2",
        "title": "Monitor box arrived punctured and screen cracked",
        "description": "The courier dropped the monitor package outside. The outer box is punctured and the LCD panel has visible cracks across the display.",
        "category_id": "cat-damaged-item",
        "order_id": "order-3",
        "status": "assigned",
        "created_by": "user-cust-3",
        "assigned_to": "user-agent-2",
        "created_at": days_ago(3),
        "updated_at": days_ago(2),
    },
    {
        "id": "ticket-3",
        "title": "Tracking says delivered but package is missing",
        "description": "Carrier tracking claims package was delivered yesterday at 3 PM, but nothing was at my door or the building mailroom.",
        "category_id": "cat-order-not-rec",
        "order_id": "order-2",
        "status": "new",
        "created_by": "user-cust-2",
        "assigned_to": None,
        "created_at": days_ago(1),
        "updated_at": days_ago(1),
    },
    {
        "id": "ticket-4",
        "title": "Please cancel duplicate order ORD-90213",
        "description": "I accidentally clicked checkout twice on my phone. Please cancel ORD-90213 before it ships out.",
        "category_id": "cat-cancel-order",
        "order_id": "order-4",
        "status": "on_hold",
        "created_by": "user-cust-1",
        "assigned_to": "user-agent-1",
        "created_at": days_ago(2),
        "updated_at": days_ago(1),
    },
    {
        "id": "ticket-5",
        "title": "Checking refund status for returned Office Chair",
        "description": "Tracking confirms warehouse received the returned chair on Monday. Could you please confirm when the $185 refund will process?",
        "category_id": "cat-refund",
        "order_id": "order-5",
        "status": "resolved",
        "created_by": "user-cust-2",
        "assigned_to": "user-agent-2",
        "created_at": days_ago(6),
        "updated_at": days_ago(1),
    },
    {
        "id": "ticket-6",
        "title": "Billed twice on credit card for keyboard",
        "description": "I noticed two identical charges of $129.99 on my Visa statement for order ORD-90211.",
        "category_id": "cat-payment-issue",
        "order_id": "order-2",
        "status": "closed",
        "created_by": "user-cust-2",
        "assigned_to": "user-agent-1",
        "created_at": days_ago(8),
        "updated_at": days_ago(3),
    },
]

# --- 5. Comments -------------------------------------------------------------
COMMENTS = [
    {
        "id": "comment-1",
        "ticket_id": "ticket-1",
        "author_id": "user-cust-1",
        "content": "I have not broken the inner seal on the accessories box. Can I get a prepaid return label?",
        "created_at": days_ago(4, 2),
    },
    {
        "id": "comment-2",
        "ticket_id": "ticket-1",
        "author_id": "user-agent-1",
        "content": "Hello Alice, I apologize for the warehouse mix-up. I've sent a return shipping label to your email and reserved a Black unit for exchange.",
        "created_at": days_ago(3, 4),
    },
    {
        "id": "comment-3",
        "ticket_id": "ticket-2",
        "author_id": "user-cust-3",
        "content": "I took photos of the box damage and the cracked panel upon opening.",
        "created_at": days_ago(3, 1),
    },
    {
        "id": "comment-4",
        "ticket_id": "ticket-4",
        "author_id": "user-agent-1",
        "content": "Placing ticket on hold while I verify with fulfillment if the parcel has already been sorted into the carrier bin.",
        "created_at": days_ago(1, 6),
    },
    {
        "id": "comment-5",
        "ticket_id": "ticket-5",
        "author_id": "user-agent-2",
        "content": "The refund of $185.00 has been initiated back to your original payment card. It typically reflects within 2-3 business days.",
        "created_at": days_ago(1, 2),
    },
    {
        "id": "comment-6",
        "ticket_id": "ticket-6",
        "author_id": "user-agent-1",
        "content": "We voided the duplicate authorization code. The pending duplicate hold has been released.",
        "created_at": days_ago(3, 1),
    },
]

# --- 6. Attachments ----------------------------------------------------------
ATTACHMENTS = [
    {
        "id": "attachment-1",
        "ticket_id": "ticket-1",
        "uploaded_by": "user-cust-1",
        "filename": "silver_headphones_box.jpg",
        "url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
        "size": 348160,
        "created_at": days_ago(4, 1),
    },
    {
        "id": "attachment-2",
        "ticket_id": "ticket-2",
        "uploaded_by": "user-cust-3",
        "filename": "cracked_monitor_panel.jpg",
        "url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf",
        "size": 524288,
        "created_at": days_ago(3, 1),
    },
    {
        "id": "attachment-3",
        "ticket_id": "ticket-6",
        "uploaded_by": "user-cust-2",
        "filename": "bank_statement_duplicate_charge.pdf",
        "url": "https://files.example.com/bank_statement_duplicate_charge.pdf",
        "size": 112640,
        "created_at": days_ago(8, 2),
    },
]

# --- 7. Audit Logs -----------------------------------------------------------
AUDIT_LOGS = [
    {
        "id": "audit-1",
        "ticket_id": "ticket-1",
        "action": "created",
        "performed_by": "user-cust-1",
        "details": "Ticket created with status 'new'.",
        "created_at": days_ago(4, 5),
    },
    {
        "id": "audit-2",
        "ticket_id": "ticket-1",
        "action": "assigned",
        "performed_by": "user-lead-1",
        "details": "Assigned to user 'user-agent-1'. Status moved from 'new' to 'assigned'.",
        "created_at": days_ago(4, 2),
    },
    {
        "id": "audit-3",
        "ticket_id": "ticket-1",
        "action": "status_changed",
        "performed_by": "user-agent-1",
        "details": "Status changed from 'assigned' to 'in_progress'.",
        "created_at": days_ago(3, 4),
    },
    {
        "id": "audit-4",
        "ticket_id": "ticket-2",
        "action": "created",
        "performed_by": "user-cust-3",
        "details": "Ticket created with status 'new'.",
        "created_at": days_ago(3, 3),
    },
    {
        "id": "audit-5",
        "ticket_id": "ticket-2",
        "action": "assigned",
        "performed_by": "user-lead-1",
        "details": "Assigned to user 'user-agent-2'. Status moved from 'new' to 'assigned'.",
        "created_at": days_ago(2, 6),
    },
    {
        "id": "audit-6",
        "ticket_id": "ticket-3",
        "action": "created",
        "performed_by": "user-cust-2",
        "details": "Ticket created with status 'new'.",
        "created_at": days_ago(1, 4),
    },
    {
        "id": "audit-7",
        "ticket_id": "ticket-4",
        "action": "status_changed",
        "performed_by": "user-agent-1",
        "details": "Status changed from 'in_progress' to 'on_hold'.",
        "created_at": days_ago(1, 6),
    },
    {
        "id": "audit-8",
        "ticket_id": "ticket-5",
        "action": "status_changed",
        "performed_by": "user-agent-2",
        "details": "Status changed from 'in_progress' to 'resolved'.",
        "created_at": days_ago(1, 2),
    },
    {
        "id": "audit-9",
        "ticket_id": "ticket-6",
        "action": "status_changed",
        "performed_by": "user-cust-2",
        "details": "Status changed from 'resolved' to 'closed'.",
        "created_at": days_ago(3, 1),
    },
]


def seed() -> None:
    """Clears the 7 collections and inserts the e-commerce seed data."""
    collections_and_data = [
        ("users", USERS),
        ("categories", CATEGORIES),
        ("orders", ORDERS),
        ("tickets", TICKETS),
        ("comments", COMMENTS),
        ("attachments", ATTACHMENTS),
        ("audit_logs", AUDIT_LOGS),
    ]

    print("--- Starting database seeding ---")
    for collection_name, documents in collections_and_data:
        collection = database[collection_name]
        deleted = collection.delete_many({}).deleted_count
        collection.insert_many(documents)
        print(f"[{collection_name}]: removed {deleted} old record(s), inserted {len(documents)} new record(s)")
    print("--- Seeding successfully finished ---")


if __name__ == "__main__":
    seed()
