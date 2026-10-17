from typing import Any
from dataclasses import dataclass, asdict


@dataclass
class HealthCheckResult:
    name: str
    is_healthy: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReadinessResponse:
    status: str
    components: list[HealthCheckResult]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)