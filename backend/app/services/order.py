from app.interfaces.order_service import IOrderService
from app.repositories import OrderRepository, StockRespository
from app.core.exceptions import NotFoundError, SoldoutError
from app.models import Order, OrderItem, Stock
from app.schemas.order import *


class OrderService(IOrderService):

    _order_repository: OrderRepository
    _stock_repository: StockRespository

    def __init__(self, order_repository: OrderRepository, stock_repository: StockRespository):
        self._order_repository = order_repository
        self._stock_repository = stock_repository

    def create_order(self, command: OrderCreate) -> OrderResponse:
        pickup_no = self._generate_pickup_num()
        items_data = self._process_items(command.items)
        new_order = self._create_order_obj(pickup_no, items_data)
        return OrderResponse.model_validate(self._persist_order(new_order))

    def _generate_pickup_num(self) -> int:
        return (self._order_repository.get_max_pickup() or 0) + 1

    def _process_items(self, items_req: list[OrderItemCreateRequest]) -> ProcessedItemsResult:
        result = ProcessedItemsResult(total_price=0, order_items=[], summaries=[])
        for item_req in items_req:
            item_res = self._process_single_item(item_req)
            result.total_price += item_res.price
            result.order_items.append(item_res.order_item)
            result.summaries.append(item_res.summary)
        return result

    def _process_single_item(self, item_req: OrderItemCreateRequest) -> ProcessedItemData:
        stock = self._get_and_validate_stock(item_req.name)
        deduct_qty = min(item_req.quantity, stock.stock)
        
        stock.stock -= deduct_qty
        self._stock_repository.update_partial(stock, {"stock": stock.stock})
        
        return ProcessedItemData(
            price=stock.price * deduct_qty,
            summary=f"{item_req.name}x{deduct_qty}",
            order_item=self._create_item_obj(item_req.name, stock.price, deduct_qty)
        )

    def _get_and_validate_stock(self, name: str) -> Stock:
        stock = self._stock_repository.find_by_name_for_update(name)
        if not stock:
            raise NotFoundError(f"{name} 不存在")
        if stock.soldout:
            raise SoldoutError(f"{name} 已售完")
        return stock

    def _create_item_obj(self, name: str, price: int, quantity: int) -> OrderItem:
        return OrderItem(
            id=None, order_id=0, name=name, price=price, quantity=quantity
        )

    def _create_order_obj(self, pickup_no: int, items_data: ProcessedItemsResult) -> Order:
        return Order(
            pickup_no=pickup_no,
            total=items_data.total_price,
            items_summary=self._build_summary(items_data.summaries),
            items=items_data.order_items
        )

    def _build_summary(self, summaries: list[str]) -> str:
        text = ", ".join(summaries)
        return text if len(text) <= 200 else text[:197] + "..."

    def _persist_order(self, order: Order) -> Order:
        saved_order = self._order_repository.create(order)
        self._order_repository.commit()
        self._order_repository.refresh(saved_order)
        return saved_order

    def get_orders(self) -> ...:
            ...
    
    def get_specific_order(self) -> ...:
        ...

    def change_status(self) -> ...:
        ...