from sqlalchemy import select

from src.auth.models import User
from src.core.repository import RepositoryBase


class UserRepository(RepositoryBase[User]):
    model = User

    async def get_user_by_email(self, *, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        session_user = await self.session.scalars(statement)
        return session_user.first()
