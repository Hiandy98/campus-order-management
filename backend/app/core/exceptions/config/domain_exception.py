from typing import Any


class DomainException(Exception):
    def __init__(self, detail: Any, status_code: int = 500):
        super().__init__(str(detail))
        self._status_code = status_code
        self._detail = detail

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def detail(self) -> Any:
        return self._detail


__all__ = ["DomainException"]