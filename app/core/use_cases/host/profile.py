from app.core.repositories import HostProfileInterface
from app.api.schemas import HostProfileSchema, HostProfileUpdateSchema
from app.core.entities import HostProfileUpdateEntity

class HostProfileUseCase:
    def __init__(
            self,
            host_profile_repo:HostProfileInterface
    ):
        self.host_profile_repo = host_profile_repo

    async def get_profile_details(self, user_id: str)->HostProfileSchema:
        profile_details = await self.host_profile_repo.get(user_id)
        if not profile_details:
            raise ValueError("No host profile details available for the given user id")
        return profile_details

    async def update_profile(self, user_id: str, update_data: HostProfileUpdateSchema)->bool:
        """Update host profile for the given user"""
        # Convert schema to entity for cleaner handling
        profile_entity = HostProfileUpdateEntity(**update_data.model_dump())
        
        return await self.host_profile_repo.update_profile(
            user_id=user_id,
            update_data=profile_entity
        )