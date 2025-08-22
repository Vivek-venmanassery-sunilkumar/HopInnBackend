from app.core.repositories import TravellerProfileInterface
from app.api.schemas import TravellerProfile
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.users.user import User as UserModel
from sqlalchemy.future import select
import logging
logger = logging.getLogger(__name__)

class TravellerProfileImpl(TravellerProfileInterface):
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def get(self, user_id: str)->TravellerProfile:
        profile_data = await self.session.scalar(
            select(UserModel).where(UserModel.id == int(user_id))
        )

        if not profile_data:
            return 
        logger.info(f'I am the logger inside traveller profile: {profile_data}')
        name_arr =(profile_data.full_name).split(' ')
        logger.info(name_arr)
        first_name = name_arr[0]
        last_name = ' '.join(name_arr[1:])
        
        return TravellerProfile(
            firstName = first_name,
            lastName=last_name,
            email=profile_data.email,
            phoneNumber=profile_data.phone_number
        )