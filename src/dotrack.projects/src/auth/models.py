from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from src.common.models import BaseModel, uuid_


class User(BaseModel):
    __tablename__ = "users"  # type: ignore

    id: Mapped[uuid_] = mapped_column()
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=True)

    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=expression.true(), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default=expression.false(), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
