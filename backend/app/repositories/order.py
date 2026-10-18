
from sqlalchemy.orm import Session


class OrderRepository:

    _db: Session

    def __init__(self, db: Session) -> None:
        self._db = db