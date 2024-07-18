from typing import AsyncIterator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from main import app
from src.common.models import BaseModel
from src.core.db import get_session
from tests.utils import get_superuser_token_headers, init_db

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=True,
)
TestingSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False, future=True, class_=AsyncSession
)


async def override_get_session() -> AsyncIterator[AsyncSession]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        await init_db(TestingSessionLocal)

        yield conn

        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="function")
async def db_session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        return session
