from typing import Any
from loguru import logger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import DomainException
from app.core.exceptions.error_response import ErrorResponse


class GlobalExceptionHandler:
    def __init__(self, app: FastAPI):
        self.app = app
        self._register_handlers()

    def _register_handlers(self) -> None:
        self.app.add_exception_handler(DomainException, self.handle_domain_exception)

    def handle_domain_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """全域攔截所有 DomainException 及其子類別"""
        domain_exc = self._cast_to_domain_exception(exc)
        
        self._log_exception(request, domain_exc)
        
        return self._build_json_response(
            status_code=domain_exc.status_code, 
            detail=domain_exc.detail
        )

    def _cast_to_domain_exception(self, exc: Exception) -> DomainException:
        assert isinstance(exc, DomainException)
        return exc

    def _log_exception(self, request: Request, exc: DomainException) -> None:
        error_class = exc.__class__.__name__
        logger.warning(f"[{error_class}] triggered on {request.url.path}: {exc.detail}")

    def _build_json_response(self, status_code: int, detail: Any) -> JSONResponse:
        error_response = ErrorResponse(detail=detail)
        return JSONResponse(
            status_code=status_code,
            content=error_response.to_dict()
        )
