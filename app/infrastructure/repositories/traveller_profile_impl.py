from app.core.repositories import TravellerProfileInterface
from app.api.schemas import TravellerProfileSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.users.user import User as UserModel
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

import logging
logger = logging.getLogger(__name__)

class TravellerProfileImpl(TravellerProfileInterface):
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def get(self, user_id: str)->TravellerProfileSchema:
        profile_data = await self.session.scalar(
            select(UserModel).where(UserModel.id == int(user_id))
        )

        if not profile_data:
            return 
        
        return TravellerProfileSchema(
            firstName = profile_data.first_name,
            lastName=profile_data.last_name,
            email=profile_data.email,
            phoneNumber=profile_data.phone_number,
            profileImageUrl=profile_data.profile_image
        )
    
    async def update_profile(self, user_id: str, update_data: dict)->bool:
        try:
            if not update_data:
                return False
            result = await self.session.execute(
                update(UserModel).where(UserModel.id == int(user_id)).values(**update_data).execution_options(synchronize_session='fetch')
            )
            logger.info(f'I am inside the profile implementation of update_profile, the result is: {result}')

            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.session.rollback()
            return False

    async def get_public_id(self, user_id: str)->str | None:
        public_id = await self.session.scalar(
            select(UserModel.profile_image_public_id).where(UserModel.id == int(user_id))
        )
        return public_id