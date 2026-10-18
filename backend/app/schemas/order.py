# app/schemas/order.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from app.models import OrderItem
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


class ProcessedItemData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    price: int
    summary: str
    order_item: OrderItem


class ProcessedItemsResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_price: int
    order_items: list[OrderItem]
    summaries: list[str]


class OrderItemQueryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: int
    quantity: int

class OrderQueryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    pickup_no: int
    status: str
    total: int
    items_summary: str
    created_at: datetime
    ready_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    items: List[OrderItemQueryResponse]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    cancel_reason: Optional[str] = Field(default=None, max_length=200)


__all__ = [
    "OrderCreate",
    "OrderItemCreateRequest",
    "OrderResponse",
    "ProcessedItemData",
    "ProcessedItemsResult",
    "OrderQueryResponse",
    "OrderItemQueryResponse",
    "OrderStatusUpdate"
]