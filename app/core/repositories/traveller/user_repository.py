from abc import ABC, abstractmethod
from app.core.entities.user import User
from app.api.schemas.Traveller.authentication import UserRegisterSchema


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserRegisterSchema) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str)-> User | None:
        pass

    @abstractmethod
    async def verify_password(self, password: str, hashed_password: str)->bool:
        pass
