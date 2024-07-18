from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.sql import func

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


id_ = Annotated[
    int,
    mapped_column(
        primary_key=True, index=True, autoincrement=True, nullable=False, unique=True, sort_order=-999, comment="id"
    ),
]

uuid_ = Annotated[
    UUID,
    mapped_column(
        primary_key=True,
        index=True,
        server_default=func.gen_random_uuid(),
        nullable=False,
        unique=True,
        sort_order=-999,
        comment="id",
    ),
]


class BaseModel(DeclarativeBase):
    __abstract__ = True
    # metadata = MetaData(naming_convention=convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @declared_attr.directive
    def __columns__(cls) -> set[str]:
        inst = inspect(cls)
        return set([c_attr.key for c_attr in inst.mapper.column_attrs])  # type: ignore

    def __repr__(self) -> str:
        columns = ", ".join([f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith("_")])
        return f"<{self.__class__.__name__}({columns})>"


class DateTimeMixin:
    create_date: Mapped[datetime] = mapped_column(server_default=func.now(), sort_order=999, comment="created_at")
    update_date: Mapped[datetime | None] = mapped_column(onupdate=func.now(), sort_order=999, comment="updated_at")


class DeletedAtMixin:
    delete_date: Mapped[datetime | None] = mapped_column(sort_order=999, comment="deleted_at")
