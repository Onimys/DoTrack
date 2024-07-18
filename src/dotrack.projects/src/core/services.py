from abc import ABC
from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models import BaseModel
from src.core.repository import RepositoryBase

RepositoryType = TypeVar("RepositoryType", bound=RepositoryBase[BaseModel], covariant=True)


class DatabaseService(ABC, Generic[RepositoryType]):
    repository_type: Type[RepositoryType]
    _repository: RepositoryType

    def __init__(self, session: AsyncSession, model: BaseModel) -> None:
        self._repository = self.repository_type(type(model), session)

    @property
    def repository(self) -> RepositoryType:
        return self._repository
