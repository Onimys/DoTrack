from src.auth.models import User
from src.auth.repository import UserRepository
from src.core.security import verify_password
from src.core.services import DatabaseService


class UserService(DatabaseService[UserRepository]):
    repository_type = UserRepository

    async def authenticate(self, *, email: str, password: str) -> User | None:
        user = await self.repository.get_user_by_email(email=email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
