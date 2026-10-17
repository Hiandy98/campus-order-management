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
    return service.update_item(name, command)