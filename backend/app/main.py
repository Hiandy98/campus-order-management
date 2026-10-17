from fastapi import FastAPI

from app.core.global_exception_handler import GlobalExceptionHandler
from app.routers import router

app = FastAPI(title="Campus order manager backend")

app.include_router(router)
GlobalExceptionHandler(app)