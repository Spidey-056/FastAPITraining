# app/models/order.py
#
# Purpose:
#   Describes the shape of an "order" document stored in MongoDB, and
#   defines payment and delivery status enums.
#   A ticket can be linked to an order (Ticket -> Order relationship)
#   so support agents can inspect payment, delivery, and item details.

from enum import Enum


class PaymentStatus(str, Enum):
    """Possible payment statuses for an order."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class DeliveryStatus(str, Enum):
    """Possible delivery statuses for an order."""
    PENDING = "pending"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    RETURNED = "returned"
    CANCELLED = "cancelled"
