from typing import Any

from app.core.exceptions.config import DomainException


class ConflictError(DomainException):
    def __init__(self, detail: Any):
        super().__init__(detail, 409)