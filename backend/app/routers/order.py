from fastapi import APIRouter, status, Depends, Query

from app.schemas.order import OrderResponse, OrderCreate, OrderQueryResponse
from app.interfaces.order_service import IOrderService
from app.core.dependencies import get_oredr_service


router = APIRouter(prefix="/orders", tags=["Order"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(request: OrderCreate, service: IOrderService = Depends(get_oredr_service)) -> OrderResponse:
    """
    建立訂單並扣減庫存。

    ### 業務邏輯
    1. **庫存扣減**：採原子性操作，庫存不足時扣至 0 為止不拋錯。僅在初始庫存為 0 時拋出 400 (SoldoutError)。
    2. **防重機制**：同名商品不可重複傳入，須由呼叫端（前端）保證。
    3. **回應機制**：成功後回傳完整訂單物件（含 `pickup_no`），呼叫端無需二次查詢。

    ### 請求參數 (Request Body)
    - **items** (array, required): 訂單品項列表。
      - **name** (string, required): 商品名稱，上限 50 字元。
      - **quantity** (integer, required): 購買數量，須 >= 1。

    ### JSON 範例
    ```json
    {
      "items": [
        {"name": "紅茶", "quantity": 2},
        {"name": "雞排", "quantity": 1}
      ]
    }
    ```
    """
    return service.create_order(request)


@router.get("", response_model=list[OrderQueryResponse])
def get_orders(
    status: str | None = Query(
        None, 
        description="篩選狀態，多值以逗號分隔，例如: pending,ready。不傳則拉取全部。"
    ),
    service: IOrderService = Depends(get_oredr_service)
):
    return service.get_orders(status=status)


