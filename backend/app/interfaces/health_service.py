from loguru import logger

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.schemas.health import ReadinessResponse, HealthCheckResult


class IHealthCheck(ABC):
    @classmethod
    @abstractmethod
    def check_readiness(cls, db: Session) -> ReadinessResponse:
        pass


class IHealthChecker(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def _execute_check(self) -> str:
        pass

    def check(self) -> HealthCheckResult:
        try:
            message = self._execute_check()
            return self._handle_success(message)
        except Exception as e:
            return self._handle_failure(e)

    def _handle_success(self, message: str) -> HealthCheckResult:
        logger.info(f"Health check passed for component: {self.name}. Message: {message}")
        return HealthCheckResult(name=self.name, is_healthy=True, message=message)

    def _handle_failure(self, exception: Exception) -> HealthCheckResult:
        logger.exception(f"Health check failed for component: {self.name}. Error: {str(exception)}")
        return HealthCheckResult(name=self.name, is_healthy=False, message=str(exception))