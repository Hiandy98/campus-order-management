from typing import Any

from app.core.exceptions.config import DomainException


class SoldoutError(DomainException):
    def __init__(self, detail: Any):
        super().__init__(detail, 400)