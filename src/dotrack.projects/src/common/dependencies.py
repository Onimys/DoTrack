from typing import Annotated, Awaitable, Callable, Type, TypeVar

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import TokenPayload
from src.common.models import BaseModel
from src.core.db import get_session
from src.core.repository import RepositoryBase
from src.core.services import DatabaseService
from src.core.settings import settings

RepositoryType = TypeVar("RepositoryType", bound=RepositoryBase[BaseModel])
ModelService = TypeVar("ModelService", bound=DatabaseService[RepositoryBase[BaseModel]])


def get_service(
    service_type: Type[ModelService],
) -> Callable[[], Awaitable[ModelService]]:
    async def _get_service(
        session: AsyncSession = Depends(get_session),
    ) -> ModelService:
        return service_type(session, service_type.repository_type.model)  # type: ignore

    return _get_service


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(
    token: TokenDep,
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


CurrentUser = Annotated[int, Depends(get_current_user)]
