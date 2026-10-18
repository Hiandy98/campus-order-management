from abc import ABC, abstractmethod


class IOrderService(ABC):

    @abstractmethod
    def create_order(self) -> ...:
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