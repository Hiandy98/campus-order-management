from abc import ABC, abstractmethod


class IStockService(ABC):
    @abstractmethod
    def add_item(self) -> ...:
        ...

    @abstractmethod
    def get_all_stock(self) -> ...:
        ...

    @abstractmethod
    def update_item(self) -> ...:
        ...