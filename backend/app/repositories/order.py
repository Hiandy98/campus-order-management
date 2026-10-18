from sqlmodel import select, func, Session

from app.models import Order


class OrderRepository:

    _db: Session

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_max_pickup(self) -> int:
        return self._db.exec(select(func.max(Order.pickup_no))).one()