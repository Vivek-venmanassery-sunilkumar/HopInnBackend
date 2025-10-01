from app.core.repositories import GuideProfileInterface
from app.core.entities import GuideOnboardEntity
from app.api.schemas import GuideProfileSchema
import logging

logger = logging.getLogger(__name__)

class GuideProfileUseCase:
    def __init__(
            self,
            guide_profile_repo:GuideProfileInterface
    ):
        self.guide_profile_repo = guide_profile_repo

    async def get_profile_details(self, user_id: str)->GuideProfileSchema:
        profile_details = await self.guide_profile_repo.get(user_id)
        if not profile_details:
            raise ValueError("No guide profile details available for the given user id")
        return profile_details
    
    async def update_profile_details(self, user_id: str, profile_details: GuideProfileSchema)->bool:

        logger.info(f'address_details: {profile_details.address}')
        guide_data = GuideOnboardEntity(
            about=profile_details.bio,
            known_languages=profile_details.knownLanguages,
            expertise=profile_details.expertise,
            profession=profile_details.profession,
            hourly_rate = profile_details.hourlyRate,
            house_name = profile_details.address.houseName,
            landmark = profile_details.address.landmark,
            district=profile_details.address.district,
            state=profile_details.address.state,
            country=profile_details.address.country,
            pincode=profile_details.address.pincode,
            coordinates=profile_details.address.coordinates
        )
        return await self.guide_profile_repo.update_profile(user_id, guide_data)