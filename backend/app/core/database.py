from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_size=15,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,   
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autoflush=False
)

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session

__all__ = ["get_session"]