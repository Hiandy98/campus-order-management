from dataclasses import asdict

from app.interfaces.stock_service import IStockService
from app.repositories.stock import StockRespository
from app.models import Stock
from app.schemas.stock import *
from app.core.exceptions import *

class StockService(IStockService):

    _stock_repository: StockRespository

    def __init__(self, stock_repository: StockRespository):
        self._stock_repository = stock_repository

    def _is_exit_by_name(self, name: str) -> bool:
        if self._stock_repository.exists_by_name(name):
            raise ConflictError(f"商品名稱 '{name}' 已經存在")
        return True
    
    def _calculate_soldout(self, stock: int) -> bool:
        return stock <= 0
    
    def add_item(self, command: StockAddItemRequest) -> StockAddItemResponse:
        self._is_exit_by_name(command.name)

        stock_entity = self._to_stock_entity(command)

        saved_stock = self._stock_repository.create(stock_entity)
        
        return self._to_add_item_response(saved_stock)

    def _to_stock_entity(self, command: StockAddItemRequest) -> Stock:
        return Stock(
            name=command.name,
            price=command.price,
            stock=command.stock,
            soldout=self._calculate_soldout(command.stock)
        )

    def _to_add_item_response(self, stock: Stock) -> StockAddItemResponse:
        return StockAddItemResponse(
            name=stock.name, 
            price=stock.price, 
            stock=stock.stock, 
            soldout=stock.soldout
        )

    def get_all_stock(self) -> list[Product]:
        stocks = self._stock_repository.get_all()
        return [self._to_product_schema(stock) for stock in stocks]

    def _to_product_schema(self, stock: Stock) -> Product:
        return Product.model_validate(stock)

    def update_item(self, name: str, command: StockUpdateItemRequest) -> StockUpdateItemResponse:
        existing_stock = self._get_existing_stock_or_raise(name)

        update_data = self._extract_clean_update_data(command)
        
        processed_data = self._process_business_rules(update_data)
        
        updated_stock = self._stock_repository.update_partial(
            existing_stock=existing_stock, 
            update_data=processed_data
        )

        return self._to_update_item_response(updated_stock)

    def _get_existing_stock_or_raise(self, name: str) -> Stock:
        existing_stock = self._stock_repository.find_by_name(name)
        if not existing_stock:
            raise NotFoundError(f"找不到商品 '{name}'，無法進行更新")
        return existing_stock

    def _extract_clean_update_data(self, command: StockUpdateItemRequest) -> dict:
        full_dict = asdict(command)
        return {k: v for k, v in full_dict.items() if v is not None}

    def _process_business_rules(self, update_data: dict) -> dict:
        if "stock" in update_data:
            update_data["soldout"] = self._calculate_soldout(update_data["stock"])
        return update_data

    def _to_update_item_response(self, stock: Stock) -> StockUpdateItemResponse:
        return StockUpdateItemResponse(
            name=stock.name,
            price=stock.price,
            stock=stock.stock,
            soldout=stock.soldout
        )

    def remove_item(self, name: str) -> None:
        existing_stock = self._get_existing_stock_or_raise(name)
        self._stock_repository.remove(existing_stock)