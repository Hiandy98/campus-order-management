from sqlalchemy.orm import Session
from sqlmodel import col

from app.schemas.stock import Product
from app.models import Stock


class StockRespository:

    _db: Session

    def __init__(self, db: Session):
        self._db = db

    def exists_by_name(self, name: str) -> bool:
        return self._db.query(Stock).filter(col(Stock.name) == name).first() is not None

    def create(self, product: Product) -> Product:
        new_stock = Stock.model_validate(product.model_dump())
        self._db.add(new_stock)
        self._db.flush()
        self._db.refresh(new_stock)
        return Product.model_validate(new_stock)
