from typing import Any

from sqlmodel import SQLModel, Field

class Stock(SQLModel, table=True):
    __tablename__: Any = "stocks"

    name: str = Field(primary_key=True, max_length=50)
    price: int = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    soldout: bool = Field(default=False)