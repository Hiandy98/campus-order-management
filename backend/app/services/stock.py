from dataclasses import asdict

from app.interfaces.stock_service import IStockService
from app.repositories.stock import StockRespository
from app.schemas.stock import *
from app.core.exceptions import ConflictError

class StockService(IStockService):

    _stock_repository: StockRespository

    def __init__(self, stock_repository: StockRespository):
        self._stock_repository = stock_repository
    
    def add_item(self, command: StockAddItemRequest) -> StockAddItemResponse:
        self._is_exit_by_name(command.name)

        product_schema = self._to_product_schema(command)

        saved_product = self._stock_repository.create(product=product_schema)

        return self._to_add_item_response(saved_product)

    def get_all_stock(self) -> ...:
        ...

    def update_item(self) -> ...:
        ...


    def _is_exit_by_name(self, name: str) -> bool:
        if self._stock_repository.exists_by_name(name):
            raise ConflictError(f"商品名稱 '{name}' 已經存在")
        return True

    def _to_product_schema(self, command: StockAddItemRequest) -> Product:
        product_dict = asdict(command)
        product_dict["soldout"] = command.stock <= 0
        return Product.model_validate(product_dict)

    def _to_add_item_response(self, product: Product) -> StockAddItemResponse:
        return StockAddItemResponse(
            name=product.name, price=product.price, stock=product.stock, soldout=product.soldout
        )