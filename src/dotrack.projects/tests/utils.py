import uuid

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.auth.models import User
from src.core.security import get_password_hash
from src.core.settings import settings

SUPER_USER_LOGIN = "admin@mail.ru"
SUPER_USER_PASSWORD = "admin"


async def init_db(session_gen: async_sessionmaker[AsyncSession]) -> None:
    async with session_gen() as session:
        user = User()
        user.id = uuid.uuid4()
        user.email = SUPER_USER_LOGIN
        user.fullname = "admin"
        user.is_superuser = True
        user.hashed_password = get_password_hash(SUPER_USER_PASSWORD)

        session.add(user)
        await session.commit()


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": SUPER_USER_LOGIN,
        "password": SUPER_USER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
