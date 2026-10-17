from typing import Any, Sequence
from backend.app.core.exceptions.config import DomainException
from app.schemas.health import HealthCheckResult

class ServiceUnhealthyError(DomainException):
    def __init__(self, components: Sequence[HealthCheckResult]):
        serialized_data = self._serialize_components(components)
        unhealthy_detail = self._build_error_detail(serialized_data)
        
        super().__init__(detail=unhealthy_detail, status_code=503)

    def _serialize_components(self, components: Sequence[HealthCheckResult]) -> list[dict[str, Any]]:
        return [component.to_dict() for component in components]

    def _build_error_detail(self, serialized_components: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "status": "unhealthy",
            "components": serialized_components
        }
