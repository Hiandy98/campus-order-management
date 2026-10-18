from sqlmodel import select, func, Session

from app.models import Order


class OrderRepository:

    _db: Session

    def __init__(self, db: Session) -> None:
        self._db = db

    def commit(self) -> None:
        self._db.commit()

    def refresh(self, order: Order) -> None:
        self._db.refresh(order)

    def rollback(self) -> None:
        self._db.rollback()

    def get_max_pickup(self) -> int:
        return self._db.exec(select(func.max(Order.pickup_no))).one()

    def create(self, order: Order) -> Order:
        self._db.add(order)
        self._db.flush()
        return order