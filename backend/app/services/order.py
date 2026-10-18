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
        try:
            pickup_no = self._generate_pickup_num()
            items_data = self._process_items(command.items) 
            new_order = self._create_order_obj(pickup_no, items_data)
            saved_order = self._persist_order(new_order)
            self._order_repository.commit() 
            return OrderResponse.model_validate(saved_order)
        except Exception as e:
            self._order_repository.rollback() 
            raise e

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
        
        self._validate_stock_availability(stock, item_req.quantity)
        
        self._deduct_and_update_stock(stock, item_req.quantity)
        
        return ProcessedItemData(
            price=stock.price * item_req.quantity,
            summary=f"{item_req.name}x{item_req.quantity}",
            order_item=self._create_item_obj(item_req.name, stock.price, item_req.quantity)
        )

    def _validate_stock_availability(self, stock: Stock, quantity: int) -> None:
        if quantity > stock.stock:
            raise SoldoutError(f"{stock.name} 餘量不足，剩餘庫存: {stock.stock}")

    def _deduct_and_update_stock(self, stock: Stock, quantity: int) -> None:
        stock.stock -= quantity
        
        update_fields = {"stock": stock.stock}
        if self._is_soldout(stock.stock):
            update_fields["soldout"] = True
            
        self._stock_repository.update_partial(stock, update_fields)

    def _is_soldout(self, stock: int) -> bool:
        return stock <= 0

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