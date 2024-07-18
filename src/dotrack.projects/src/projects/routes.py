from fastapi import APIRouter, Depends

from src.common.dependencies import get_service
from src.projects.schemas import ProjectsSchema
from src.projects.service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectsSchema])
async def get_all_projects(service: ProjectService = Depends(get_service(ProjectService))):
    projects = await service.repository.get_all()
    return projects


class TestProject:
    def create_project(self, name: str) -> ProjectsSchema:
        return ProjectsSchema(id=1, name=name)


@router.get("/test", response_model=ProjectsSchema)
async def get_test_projects(service: TestProject = Depends()):
    return service.create_project(name="test")
