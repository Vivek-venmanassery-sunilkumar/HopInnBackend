from app.core.repositories import UserRolesPermissionsInterface
from app.core.entities import UserRolesAndPermissionsEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.database.models.users.user import User as UserModel

#Implementation that helps the route protection in the backend therefore entitiy is returned 

class UserRolesPermissionsImpl(UserRolesPermissionsInterface):
    def __init__(
            self,
            session: AsyncSession
            ):
        self.session = session
    
    async def get_user_roles_and_permissions(self, user_id: str)->UserRolesAndPermissionsEntity:
        user_data = await self.session.scalar(
            select(UserModel).where(UserModel.id == int(user_id))
        )

        return UserRolesAndPermissionsEntity(
            is_traveller=user_data.is_traveller,
            is_guide=user_data.is_guide,
            is_host=user_data.is_host,
            is_admin =user_data.is_admin,
            is_active=user_data.is_active
        )