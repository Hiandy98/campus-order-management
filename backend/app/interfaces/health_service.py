from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.schemas.health import ReadinessResponse


class IHealthCheck(ABC):
    @abstractmethod
    def check_readiness(self, db: Session) -> ReadinessResponse:
        pass