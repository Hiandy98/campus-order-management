from fastapi import Depends
from sqlalchemy.orm import Session

from app.interfaces.stock_service import IStockService
from app.services.stock import StockService
from app.repositories.stock import StockRespository
from app.core.database import get_session


def get_stock_service(db: Session = Depends(get_session)) -> IStockService:
    repo = StockRespository(db)
    return StockService(stock_repository=repo)