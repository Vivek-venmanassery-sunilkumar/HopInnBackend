from abc import ABC, abstractmethod
from app.core.entities.user_roles_and_permissions import UserRolesAndPermissions

class UserRolesPermissionsInterface(ABC):
    @abstractmethod
    async def get_user_roles_and_permissions(self, user_id: str)->UserRolesAndPermissions:
        pass
