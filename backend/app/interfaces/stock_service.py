from abc import ABC, abstractmethod
from app.schemas.stock import *


class IStockService(ABC):
    @abstractmethod
    def add_item(self, command: StockAddItemRequest) -> StockAddItemResponse:
        ...

    @abstractmethod
    def get_all_stock(self) -> list[Product]:
        ...

    @abstractmethod
    def update_item(self, name: str, command: StockUpdateItemRequest) -> StockUpdateItemResponse:
        ...