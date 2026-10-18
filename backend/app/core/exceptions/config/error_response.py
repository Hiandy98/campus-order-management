from typing import Any

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ErrorResponse:
    detail: Any

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


__all__ = ["ErrorResponse"]