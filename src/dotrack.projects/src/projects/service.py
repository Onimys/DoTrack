from src.core.services import DatabaseService
from src.projects.repository import ProjectRepository


class ProjectService(DatabaseService[ProjectRepository]):
    repository_type = ProjectRepository
