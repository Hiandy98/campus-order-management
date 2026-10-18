from abc import ABC, abstractmethod

from app.schemas.order import *


class IOrderService(ABC):

    @abstractmethod
    def create_order(self, command: OrderCreate) -> OrderResponse:
        ...

    @abstractmethod
    def get_orders(self) -> ...:
        ...

    @abstractmethod
    def get_specific_order(self) -> ...:
        ...

    @abstractmethod
    def change_status(self) -> ...:
        ...