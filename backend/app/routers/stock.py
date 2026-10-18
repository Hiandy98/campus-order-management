from fastapi import Depends, status, APIRouter

from app.interfaces.stock_service import IStockService
from app.schemas.stock import *
from app.core.dependencies import get_stock_service


router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post(
    "", response_model=StockAddItemResponse, status_code=status.HTTP_201_CREATED
)
def add_stock(
    command: StockAddItemRequest, service: IStockService = Depends(get_stock_service)
) -> StockAddItemResponse:
    """
    建立全新商品庫存。
    
    - **name**: 商品名稱 (不可重複)
    - **price**: 價格
    - **stock**: 庫存量
    """
    return service.add_item(command)

@router.patch(
    "/{name}", response_model=StockUpdateItemResponse
)
def update_product(
    name: str, command: StockUpdateItemRequest, service: IStockService = Depends(get_stock_service)
):
    """
    更新物品

    (不填則不動)

    - **price**: 價格
    - **stock**: 庫存量(非+多少庫存)
    - **soldout**: 是否開放採購
    """
    return service.update_item(name, command)

@router.get(
    "", response_model=list[Product]
)
def get_all_stock(service: IStockService = Depends(get_stock_service)):
    """
    取得已加入的商品清單與庫存量
    """
    return service.get_all_stock()

@router.delete(
    "/{name}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_by_name(name: str, service: IStockService = Depends(get_stock_service)):
    """
    刪除商品

    - **name**: 品名
    """
    return service.remove_item(name)

