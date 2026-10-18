from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.core.global_exception_handler import GlobalExceptionHandler
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
        lifespan=lifespan
    )
    
    app.include_router(router)
    
    GlobalExceptionHandler(app)
    
    return app


app = create_app()
