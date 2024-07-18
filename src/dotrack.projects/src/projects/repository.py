from src.core.repository import RepositoryBase

from .models import Projects


class ProjectRepository(RepositoryBase[Projects]):
    model = Projects
