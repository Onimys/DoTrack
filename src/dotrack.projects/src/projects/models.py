from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.models import BaseModel, DeletedAtMixin, id_


class Projects(DeletedAtMixin, BaseModel):
    __tablename__ = "projects"  # type: ignore

    id: Mapped[id_] = mapped_column()
    name: Mapped[str] = mapped_column(String(200), unique=True)
