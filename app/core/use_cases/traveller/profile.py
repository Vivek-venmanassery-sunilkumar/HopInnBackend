from app.api.schemas import TravellerProfile
from app.core.repositories import TravellerProfileInterface
import logging

logger = logging.getLogger(__name__)

class ProfileUseCase:
    def __init__(
            self,
            traveller_profile: TravellerProfileInterface
    ):
        self.traveller_profile = traveller_profile
    async def get_profile_details(self, user_id: str)->TravellerProfile: 
        profile_details = await self.traveller_profile.get(user_id)
        logger.info(f"njn profilil und: {profile_details}")
        if not profile_details:
            return ValueError('no profile details available for the given user id')
        return profile_details        

        