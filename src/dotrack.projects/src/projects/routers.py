from fastapi import APIRouter, Depends

from src.core.db import AsyncSession, get_session
from src.projects import service
from src.projects.schemas import ProjectsSchema

router = APIRouter(prefix="/repo/projects")


@router.get("/", response_model=list[ProjectsSchema])
async def get_all_projects(session: AsyncSession = Depends(get_session)):
    projects = await service.get_all_projects(session)
    return projects
