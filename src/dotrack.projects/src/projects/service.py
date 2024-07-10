from typing import Sequence

from sqlalchemy import select

from src.core.db import AsyncSession
from src.projects.models import Projects


async def get_all_projects(session: AsyncSession) -> Sequence[Projects]:
    result = await session.execute(select(Projects))
    return result.scalars().all()
