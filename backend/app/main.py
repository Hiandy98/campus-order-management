from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.core.global_exception_handler import GlobalExceptionHandler
from app.core.config import settings
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() 
    #...
    yield
    #...
    pass


def create_app() -> FastAPI:
    app = FastAPI(
        title="Campus order manager backend",
        lifespan=lifespan,
        debug=settings.is_development,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    app.include_router(router)
    
    GlobalExceptionHandler(app)
    
    return app


app = create_app()
