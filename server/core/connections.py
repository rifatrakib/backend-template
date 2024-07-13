from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from server.core.config import settings


@lru_cache()
def connection_pool() -> AsyncEngine:
    engine = create_async_engine(
        settings.RDS_URI,
        pool_size=10,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
    )
    return engine


def get_database_session() -> AsyncSession:
    engine = connection_pool()
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return Session()
