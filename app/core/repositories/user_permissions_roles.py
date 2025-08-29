from abc import ABC, abstractmethod
from app.core.entities import UserRolesAndPermissionsEntity

class UserRolesPermissionsInterface(ABC):
    @abstractmethod
    async def get_user_roles_and_permissions(self, user_id: str)->UserRolesAndPermissionsEntity:
        pass
