from typing import Any, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from app.models.order_status import OrderStatus

if TYPE_CHECKING:
    from app.models.order_item import OrderItem


class Order(SQLModel, table=True):
    __tablename__: Any = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    pickup_no: int = Field(unique=True, index=True)
    status: OrderStatus = Field(default=OrderStatus.PENDING, index=True)
    total: int = Field(ge=0)

    # summary = ", ".join(f"{i.name}x{i.qty}" for i in items)
    items_summary: str = Field(max_length=200)   

    created_at: datetime = Field(default_factory=datetime.now, index=True)
    ready_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancel_reason: Optional[str] = Field(default=None, max_length=200)

    items: list["OrderItem"] = Relationship(
        back_populates="order",
        cascade_delete=True,
    )