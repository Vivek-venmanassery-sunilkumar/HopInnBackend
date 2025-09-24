from app.core.repositories import UserRolesPermissionsInterface
from app.core.entities import UserRolesAndPermissionsEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infrastructure.database.models.users.user import User as UserModel
from app.infrastructure.database.models.onboard import Guide, Host

#Implementation that helps the route protection in the backend therefore entitiy is returned 

class UserRolesPermissionsImpl(UserRolesPermissionsInterface):
    def __init__(
            self,
            session: AsyncSession
            ):
        self.session = session
    
    async def get_user_roles_and_permissions(self, user_id: str)->UserRolesAndPermissionsEntity:
        query = (
            select(UserModel, Guide.is_blocked.label('guide_is_blocked'), Host.is_blocked.label('host_is_blocked'))
            .outerjoin(Guide, Guide.user_id == UserModel.id)
            .outerjoin(Host, Host.user_id == UserModel.id)
            .where(UserModel.id == int(user_id))
        )
        result = await self.session.execute(query)
        row = result.first()
        user_data, guide_is_blocked, host_is_blocked = row 

        return UserRolesAndPermissionsEntity(
            is_traveller=user_data.is_traveller,
            is_guide=user_data.is_guide,
            is_host=user_data.is_host,
            is_admin =user_data.is_admin,
            is_active=user_data.is_active,
            is_guide_blocked=guide_is_blocked,
            is_host_blocked=host_is_blocked
        )