from app.api.schemas import TravellerProfileSchema
from app.core.entities import TravellerUpdateProfileEntity
from app.core.repositories import TravellerProfileInterface
import logging

logger = logging.getLogger(__name__)

class ProfileUseCase:
    def __init__(
            self,
            traveller_profile: TravellerProfileInterface,
    ):
        self.traveller_profile = traveller_profile

    async def get_profile_details(self, user_id: str)->TravellerProfileSchema: 
        profile_details = await self.traveller_profile.get(user_id)
        logger.info(f"njn profilil und: {profile_details}")
        if not profile_details:
            raise ValueError('no profile details available for the given user id')
        return profile_details        

    async def update_profile_details(self, user_id: str, update_details: TravellerProfileSchema)->bool:
        entity_update_data = TravellerUpdateProfileEntity(**update_details.model_dump())
        update_data = entity_update_data.model_dump(exclude_none=True, by_alias=False)


        if not update_data:
            raise ValueError("No fields to update")
        
        updated_profile = await self.traveller_profile.update_profile(
            user_id = user_id, 
            update_data = update_data
        )

        if not updated_profile:
            raise ValueError("Profile not found or update failed")
        
        return True
    
    async def get_public_id(self, user_id: str)->str | None:
        return await self.traveller_profile.get_public_id(user_id)
        