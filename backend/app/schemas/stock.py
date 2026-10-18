from typing import Optional

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


@dataclass(frozen=True)
class StockUpdateItemRequest:
    price: Optional[int] = None
    stock: Optional[int] = None
    soldout: Optional[bool] = None

@dataclass(frozen=True)
class StockUpdateItemResponse:
    name: str
    price: int
    stock: int
    soldout: bool


__all__ = [
        "Product", 
        "StockAddItemRequest", 
        "StockAddItemResponse", 
        "StockUpdateItemRequest", 
        "StockUpdateItemResponse"
    ]