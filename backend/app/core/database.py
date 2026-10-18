from loguru import logger
from typing import Generator

from sqlmodel import SQLModel, create_engine, Session

from app.core.config import settings
from app.models import *


engine = create_engine(
    settings.database_url,
    echo=False,
    pool_size=15,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,   
    pool_pre_ping=True
)

from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autoflush=False
)

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

def create_db_and_tables():
    logger.info("Checking and creating data tables in the cloud database...")
    SQLModel.metadata.create_all(engine)
    logger.info("Data sheet check completed")

__all__ = ["get_session", "create_db_and_tables"]