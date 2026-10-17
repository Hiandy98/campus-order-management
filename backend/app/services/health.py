from loguru import logger
from typing import Sequence

from sqlmodel import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.interfaces.health_service import *
from app.schemas.health import *
from app.core.exceptions import ServiceUnhealthyError


class DataBaseHealthChecker(IHealthChecker):
    def __init__(self, db: Session):
        super().__init__(name="database")
        self.db = db

    def _execute_check(self) -> str:
        if not self._is_database_responding():
            raise RuntimeError("Database return value error")
        return "healthy"
    
    def _is_database_responding(self) -> bool:
        """透過 SELECT 1 確認資料庫是否能正常回應，並安全處理異常."""
        try:
            statement = text("SELECT 1")
            result = self.db.scalar(statement)
            return result == 1
        except SQLAlchemyError as e:
            logger.warning(f"Database query encountered SQLAlchemyError: {str(e)}")
            return False
        except Exception as e:
            logger.warning(f"Database query encountered unexpected error: {str(e)}")
            return False


class HealthCheckService(IHealthCheck):
    
    @classmethod
    def check_readiness(cls, db: Session) -> ReadinessResponse:
        components = cls._run_health_checks(db)

        if cls._has_unhealthy_component(components):
            cls._handle_unhealthy_flow(components)

        return cls._build_success_response(components)

    @classmethod
    def _run_health_checks(cls, db: Session) -> list[HealthCheckResult]:
        checkers: list[IHealthChecker] = [
            DataBaseHealthChecker(db),
            #...
        ]
        return [checker.check() for checker in checkers]

    @classmethod
    def _has_unhealthy_component(cls, components: Sequence[HealthCheckResult]) -> bool:
        return any(not component.is_healthy for component in components)

    @classmethod
    def _handle_unhealthy_flow(cls, components: list[HealthCheckResult]) -> None:
        logger.warning("Service readiness check failed. One or more components are unhealthy.")
        
        raise ServiceUnhealthyError(components=components)

    @classmethod
    def _build_success_response(cls, components: list[HealthCheckResult]) -> ReadinessResponse:
        logger.info("Service readiness check status: ready.")
        return ReadinessResponse(
            status="ready",
            components=components
        )