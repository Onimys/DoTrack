import logging
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.settings import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DB_URI,
    echo=settings.ECHO_SQL,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False, future=True, class_=AsyncSession
)


# Dependency
async def get_session() -> AsyncIterator[AsyncSession]:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        logger.exception(e)
