from typing import Any

from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: int
    stock: int
    soldout: bool


@dataclass(frozen=True)
class StockAddItemRequest:
    name: str
    price: int
    stock: int

@dataclass(frozen=True)
class StockAddItemResponse:
    name: str
    price: int
    stock: int
    soldout: bool