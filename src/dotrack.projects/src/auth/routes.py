from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.schemas import Token, UserPublic
from src.auth.service import UserService
from src.common.dependencies import CurrentUser, get_service
from src.core import security

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserService = Depends(get_service(UserService))
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await service.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return Token(access_token=security.create_access_token(user.id, UserPublic(**user.__dict__).model_dump()))


@router.post("/token/test", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
