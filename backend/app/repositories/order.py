from typing import List, Any, cast, Sequence

from sqlmodel import select, func, Session
from sqlalchemy.orm import selectinload

from app.models import Order


class OrderRepository:

    _db: Session

    def __init__(self, db: Session) -> None:
        self._db = db

    def refresh(self, order: Order) -> None:
        self._db.refresh(order)

    def get_max_pickup(self) -> int:
        result = self._db.exec(select(func.max(Order.pickup_no))).first()
        return result if result is not None else 0

    def create(self, order: Order) -> Order:
        self._db.add(order)
        self._db.flush()
        return order

    def get_all_with_items(self) -> list[Order]:
        statement = select(Order).options(
            selectinload(cast(Any, Order.items))
        )
        result = self._db.exec(statement)
        return list(result.all())