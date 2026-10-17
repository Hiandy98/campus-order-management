from sqlalchemy.orm import Session
from sqlmodel import col, select

from app.schemas.stock import Product
from app.models import Stock


class StockRespository:

    _db: Session

    def __init__(self, db: Session):
        self._db = db

    def commit(self) -> None:
        self._db.commit()

    def exists_by_name(self, name: str) -> bool:
        return self._db.query(Stock).filter(col(Stock.name) == name).first() is not None

    def find_by_name(self, name: str) -> Stock | None:
        return self._db.query(Stock).filter(col(Stock.name) == name).first()

    def create(self, product: Product) -> Product:
        new_stock = Stock.model_validate(product.model_dump())
        self._db.add(new_stock)
        self._db.flush()
        self._db.refresh(new_stock)
        return Product.model_validate(new_stock)

    def update_partial(self, existing_stock: Stock, update_data: dict) -> Product:
        existing_stock.sqlmodel_update(update_data)
        
        self._db.add(existing_stock)
        self._db.flush()
        self._db.refresh(existing_stock)
        
        return Product.model_validate(existing_stock)

    def get_all(self) -> list[Product]:
        stocks = self._db.scalars(select(Stock)).all()
        return [Product.model_validate(stock) for stock in stocks]
