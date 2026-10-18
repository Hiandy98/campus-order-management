from sqlmodel import col, select, Session
from app.models import Stock

class StockRespository:

    _db: Session

    def __init__(self, db: Session):
        self._db = db

    def exists_by_name(self, name: str) -> bool:
        statement = select(Stock).where(col(Stock.name) == name)
        return self._db.exec(statement).first() is not None

    def find_by_name(self, name: str) -> Stock | None:
        statement = select(Stock).where(col(Stock.name) == name)
        return self._db.exec(statement).first()

    def create(self, stock: Stock) -> Stock:
        self._db.add(stock)
        self._db.flush()
        self._db.refresh(stock)
        return stock

    def update_partial(self, existing_stock: Stock, update_data: dict) -> Stock:
        existing_stock.sqlmodel_update(update_data)
        self._db.add(existing_stock)
        self._db.flush()
        self._db.refresh(existing_stock) 
        return existing_stock

    def get_all(self) -> list[Stock]:
        return list(self._db.exec(select(Stock)).all())

    def remove(self, stock: Stock) -> None:
        self._db.delete(stock)
        self._db.flush()

    def find_by_name_for_update(self, name: str) -> Stock | None:
        statement = select(Stock).where(col(Stock.name) == name).with_for_update()
        return self._db.exec(statement).first()