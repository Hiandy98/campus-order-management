from fastapi import Depends
from sqlmodel import Session

from app.interfaces.order_service import IOrderService
from app.services.order import OrderService
from app.repositories import OrderRepository, StockRespository
from app.core.database import get_session


def get_oredr_service(db: Session = Depends(get_session)) -> IOrderService:
    stock_repository = StockRespository(db)
    order_repository = OrderRepository(db)
    return OrderService(
        order_repository=order_repository, stock_repository=stock_repository
    )