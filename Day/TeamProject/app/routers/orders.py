# app/routers/orders.py
#
# Purpose:
#   HTTP endpoints for the Order entity.
#   POST   /orders                  -> create an order
#   GET    /orders                  -> list orders (optional filter by customer_id)
#   GET    /orders/{order_id}       -> get a single order
#   PUT    /orders/{order_id}       -> update order details / statuses
#   DELETE /orders/{order_id}       -> remove an order
#   GET    /orders/{order_id}/tickets -> list tickets linked to this order

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.collection import Collection

from app.dependencies import (
    get_orders_collection,
    get_users_collection,
    get_tickets_collection,
)
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.schemas.ticket import TicketResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    orders_collection: Collection = Depends(get_orders_collection),
    users_collection: Collection = Depends(get_users_collection),
):
    """
    Create a new customer order.
    POST -> create, per REST convention.
    """
    # Enforce customer existence
    if not users_collection.find_one({"id": payload.customer_id}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="customer_id does not match any existing user.",
        )

    # Enforce unique order_number
    if orders_collection.find_one({"order_number": payload.order_number}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An order with this order_number already exists.",
        )

    now = datetime.utcnow()
    order_doc = {
        "id": str(uuid4()),
        "order_number": payload.order_number,
        "customer_id": payload.customer_id,
        "items": [item.model_dump() for item in payload.items],
        "total_amount": payload.total_amount,
        "payment_status": payload.payment_status,
        "delivery_status": payload.delivery_status,
        "created_at": now,
        "updated_at": now,
    }
    orders_collection.insert_one(order_doc)
    return order_doc


@router.get("", response_model=List[OrderResponse])
def list_orders(
    orders_collection: Collection = Depends(get_orders_collection),
    customer_id: Optional[str] = Query(default=None, description="Filter orders by customer user id"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    """List orders with optional customer_id filter and pagination."""
    mongo_filter = {}
    if customer_id is not None:
        mongo_filter["customer_id"] = customer_id

    cursor = orders_collection.find(mongo_filter).sort("created_at", -1).skip(skip).limit(limit)
    return list(cursor)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    orders_collection: Collection = Depends(get_orders_collection),
):
    """Get a single order by id."""
    order_doc = orders_collection.find_one({"id": order_id})
    if not order_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order_doc


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: str,
    payload: OrderUpdate,
    orders_collection: Collection = Depends(get_orders_collection),
):
    """Update order details or statuses (e.g. payment_status, delivery_status)."""
    existing = orders_collection.find_one({"id": order_id})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        return existing

    if "items" in update_data and update_data["items"] is not None:
        update_data["items"] = [item.model_dump() if hasattr(item, "model_dump") else item for item in update_data["items"]]

    update_data["updated_at"] = datetime.utcnow()
    orders_collection.update_one({"id": order_id}, {"$set": update_data})
    return orders_collection.find_one({"id": order_id})


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: str,
    orders_collection: Collection = Depends(get_orders_collection),
):
    """Delete an order by id."""
    result = orders_collection.delete_one({"id": order_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return None


@router.get("/{order_id}/tickets", response_model=List[TicketResponse])
def list_tickets_for_order(
    order_id: str,
    orders_collection: Collection = Depends(get_orders_collection),
    tickets_collection: Collection = Depends(get_tickets_collection),
):
    """List all support tickets associated with this specific order."""
    if not orders_collection.find_one({"id": order_id}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    tickets = list(tickets_collection.find({"order_id": order_id}).sort("created_at", -1))
    return tickets
