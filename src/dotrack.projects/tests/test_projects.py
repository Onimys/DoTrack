from pytest_mock import MockFixture
from sqlalchemy.ext.asyncio import AsyncSession

from src.projects.models import Projects
from src.projects.repository import ProjectRepository
from src.projects.schemas import CreateProjectSchema


async def test_crud_projects(db_session: AsyncSession) -> None:
    repository = ProjectRepository(Projects, db_session)

    projects = await repository.get_all()
    assert len(projects) == 0

    new_project = CreateProjectSchema(
        name="test",
    )
    new_project = await repository.create(new_project.model_dump())

    projects = await repository.get_all()
    assert len(projects) == 1

    await repository.delete(Projects.id == new_project.id)

    projects = await repository.get_all()
    assert len(projects) == 0


async def test_patch_projects(db_session: AsyncSession, mocker: MockFixture) -> None:
    obj = mocker.patch.object(ProjectRepository, "get_all", return_value=[1])
    repository = ProjectRepository(Projects, db_session)

    projects = await repository.get_all()

    assert len(projects) == 1
    obj.assert_called_once()
