from abc import ABC, abstractmethod
from app.core.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str)-> User | None:
        pass