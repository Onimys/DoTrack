import uuid
from typing import Any, Generic, Type, TypeVar

from sqlalchemy import BinaryExpression, ColumnElement, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel, covariant=True)


class RepositoryBase(Generic[ModelType]):
    """Repository for performing database queries."""

    model: Type[ModelType]

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, data: dict[Any, Any]) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, pk: uuid.UUID | int) -> ModelType | None:
        return await self.session.get(self.model, pk)

    async def get_all(self) -> list[ModelType]:
        query = select(self.model)
        return list(await self.session.scalars(query))

    async def filter(
        self,
        *expressions: BinaryExpression[Any] | ColumnElement[Any],
    ) -> list[ModelType]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))

    async def delete(
        self,
        *expressions: BinaryExpression[Any] | ColumnElement[Any],
    ) -> None:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)

        for item in await self.session.scalars(query):
            await self.session.delete(item)
        await self.session.commit()
