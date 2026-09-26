# app/schemas/order.py
#
# Purpose:
#   Defines the Pydantic models for the Order entity.
#   Orders represent customer purchases that support tickets are linked to.

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.order import PaymentStatus, DeliveryStatus


class OrderItem(BaseModel):
    """Represents a single product/item within an order."""
    name: str = Field(..., min_length=1, max_length=200, description="Item name")
    quantity: int = Field(default=1, gt=0, description="Quantity ordered")
    price: float = Field(..., ge=0, description="Unit price of the item")


class OrderCreate(BaseModel):
    """Data required from the client when recording a new order (POST /orders)."""
    order_number: str = Field(..., min_length=3, max_length=50, description="Human-readable order identifier, e.g. 'ORD-10023'")
    customer_id: str = Field(..., description="id of the User (customer) who placed the order")
    items: List[OrderItem] = Field(default_factory=list, description="List of items in the order")
    total_amount: float = Field(..., ge=0, description="Total order amount")
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING, description="Payment status")
    delivery_status: DeliveryStatus = Field(default=DeliveryStatus.PENDING, description="Delivery status")


class OrderUpdate(BaseModel):
    """
    Data a client MAY send when updating an order (PUT /orders/{id}).
    Allows updating status, items, or amount.
    """
    items: Optional[List[OrderItem]] = Field(default=None)
    total_amount: Optional[float] = Field(default=None, ge=0)
    payment_status: Optional[PaymentStatus] = Field(default=None)
    delivery_status: Optional[DeliveryStatus] = Field(default=None)


class OrderResponse(BaseModel):
    """Shape of an order as returned by the API."""
    id: str
    order_number: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    payment_status: PaymentStatus
    delivery_status: DeliveryStatus
    created_at: datetime
    updated_at: datetime
