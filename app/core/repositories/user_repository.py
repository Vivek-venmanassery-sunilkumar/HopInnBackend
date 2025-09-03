from abc import ABC, abstractmethod
from app.core.entities import UserEntity,AdminCreationEntity
from app.api.schemas import UserRolesSchema,UserRegisterSchema

class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserRegisterSchema) -> UserEntity:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str)-> UserEntity | None:
        pass

    @abstractmethod
    async def verify_password(self, password: str, hashed_password: str)->bool:
        pass

    @abstractmethod
    async def get_user_roles(self, user_id: str)->UserRolesSchema:
        pass
    

    @abstractmethod
    async def create_admin_user(self, admin_data: AdminCreationEntity)->bool:
        pass


    @abstractmethod
    async def does_user_exist(self, email: str)->bool:
        pass

    @abstractmethod
    async def verify_google_token(self, google_token: str)->dict:
        pass

    @abstractmethod
    async def update_google_user_info(self, email: str, google_id: str, picture: str)->UserEntity:
        pass

    @abstractmethod
    async def create_google_user(self, email: str, name: str, google_id: str, picture: str)->UserEntity:
        pass