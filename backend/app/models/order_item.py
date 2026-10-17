from typing import Any, Optional

from sqlmodel import SQLModel, Field


class OrderItem(SQLModel, table=True):
    __tablename__: Any = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    name: str = Field(max_length=50, index=True)
    price: int = Field(ge=0)
    quantity: int = Field(ge=1)