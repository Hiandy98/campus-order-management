# app/schemas/order.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.models.order_status import OrderStatus


class OrderItemCreateRequest(BaseModel):
    name: str = Field(..., max_length=50)
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    items: List[OrderItemCreateRequest]


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: int
    quantity: int


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    pickup_no: int
    status: OrderStatus
    total: int
    items_summary: str
    created_at: datetime
    ready_at: Optional[datetime]
    completed_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    cancel_reason: Optional[str]
    items: List[OrderItemResponse]


__all__ = [
    "OrderCreate",
    "OrderResponse"
]