from datetime import datetime
from pydantic import NaiveDatetime

from app.interfaces.order_service import IOrderService
from app.repositories import OrderRepository, StockRespository
from app.core.exceptions import NotFoundError, SoldoutError, InvalidStatusTransitionError
from app.models import Order, OrderItem, Stock
from app.models.order_status import OrderStatus
from app.schemas.order import (
        OrderCreate, OrderResponse, OrderItemCreateRequest, 
        OrderQueryResponse, ProcessedItemsResult, ProcessedItemData, OrderStatusUpdate
    )


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
        saved_order = self._persist_order(new_order)
        return OrderResponse.model_validate(saved_order)

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
        
        if stock.price <= 0:
            raise ValueError(f"商品 {stock.name} 價格異常 ({stock.price})，無法下單")

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
            id=None, order_id=None, name=name, price=price, quantity=quantity
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
        self._order_repository.refresh(saved_order)
        return saved_order

    def get_orders(self, status: str | None = None) -> list[OrderQueryResponse]:
        all_orders = self._order_repository.get_all_with_items()
        target_statuses = self._parse_status_param(status)
        filtered_orders = self._filter_orders_by_statuses(all_orders, target_statuses)
        sorted_orders = self._sort_orders_by_business_rules(filtered_orders, target_statuses)
        return self._to_query_responses(sorted_orders)

    def _parse_status_param(self, status: str | None = None) -> list[str]:
        if not status:
            return []
        return [s.strip() for s in status.split(",") if s.strip()]

    def _filter_orders_by_statuses(self, orders: list[Order], statuses: list[str]) -> list[Order]:
        if not statuses:
             return orders
        return [o for o in orders if o.status in statuses]

    def _sort_orders_by_business_rules(self, orders: list[Order], statuses: list[str]) -> list[Order]:
        if statuses == [OrderStatus.READY]:
            return sorted(
                orders, 
                key=lambda o: o.ready_at if o.ready_at is not None else o.created_at
            )
        return sorted(orders, key=lambda o: o.created_at)

    def _to_query_responses(self, orders: list[Order]) -> list[OrderQueryResponse]:
        return [OrderQueryResponse.model_validate(order) for order in orders]

    def get_specific_order(self) -> ...:
        ...

    def change_status(self, order_id: int, command: OrderStatusUpdate) -> OrderResponse:
        order = self._get_order_for_update(order_id)
        self._validate_status_transition(order, command)

        update_fields = self._build_status_update_fields(command)
        self._order_repository.update_partial(order, update_fields)

        return OrderResponse.model_validate(order)

    def _get_order_for_update(self, order_id: int) -> Order:
        order = self._order_repository.get_by_id_for_update(order_id)
        if order is None:
            raise NotFoundError(f"訂單 {order_id} 不存在")
        return order

    def _validate_status_transition(
        self, order: Order, command: OrderStatusUpdate
    ) -> None:
        current = order.status
        target = command.status

        if not current.can_transition_to(target):
            raise InvalidStatusTransitionError(
                f"非法狀態轉移：{current.value} → {target.value}"
            )

        if target == OrderStatus.CANCELLED and not command.cancel_reason:
            raise InvalidStatusTransitionError("取消訂單必須提供 cancel_reason")

    def _build_status_update_fields(
        self, command: OrderStatusUpdate
    ) -> dict:
        now: NaiveDatetime = datetime.now()
        target = command.status

        update: dict = {"status": target}

        if target == OrderStatus.READY:
            update["ready_at"] = now
        elif target == OrderStatus.COMPLETED:
            update["completed_at"] = now
        elif target == OrderStatus.CANCELLED:
            update["cancelled_at"] = now
            update["cancel_reason"] = command.cancel_reason

        return update