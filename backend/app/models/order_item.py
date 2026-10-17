from typing import Any, Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.order import Order


class OrderItem(SQLModel, table=True):
    __tablename__: Any = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(
        foreign_key="orders.id",
        index=True,
        ondelete="CASCADE",
    )
    name: str = Field(max_length=50, index=True)
    price: int = Field(ge=0)
    quantity: int = Field(ge=1)

    order: Optional["Order"] = Relationship(back_populates="items")