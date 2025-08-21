from app.core.repositories import UserRolesPermissionsInterface
from app.core.entities.user_roles_and_permissions import UserRolesAndPermissions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.database.models.users.user import User as UserModel

class UserRolesPermissionsImpl(UserRolesPermissionsInterface):
    def __init__(
            self,
            session: AsyncSession
            ):
        self.session = session
    
    async def get_user_roles_and_permissions(self, user_id: str)->UserRolesAndPermissions:
        user_data = await self.session.scalar(
            select(UserModel).where(user_id = int(user_id))
        )

        return UserRolesAndPermissions(
            is_traveller=user_data.is_traveller,
            is_guide=user_data.is_guide,
            is_host=user_data.is_host,
            is_admin =user_data.is_admin,
            is_active=user_data.is_active
        )