from datetime import datetime

from pydantic import ConfigDict

from src.common.schema import SchemaBase


class ProjectSchemaBase(SchemaBase):
    name: str


class CreateProjectSchema(ProjectSchemaBase):
    pass


class UpdateProjectSchema(ProjectSchemaBase):
    pass


class ProjectsSchema(ProjectSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    delete_date: datetime | None = None
