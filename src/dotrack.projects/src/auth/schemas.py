from uuid import UUID

from pydantic import EmailStr, Field

from src.common.schema import SchemaBase


class Token(SchemaBase):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SchemaBase):
    sub: UUID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserBase(SchemaBase):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    email: EmailStr | None = None  # type: ignore
    password: str | None = None


class UpdatePassword(SchemaBase):
    current_password: str
    new_password: str


class UserRegister(SchemaBase):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserPublic(UserBase):
    id: UUID


class User(UserBase):
    id: UUID | None = None
    hashed_password: str
