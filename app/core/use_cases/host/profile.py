from app.core.repositories import HostProfileInterface
from app.api.schemas import HostProfileSchema

class HostProfileUseCase:
    def __init__(
            self,
            host_profile_repo:HostProfileInterface
    ):
        self.host_profile_repo = host_profile_repo

    async def get_profile_details(self, user_id: str)->HostProfileSchema:
        profile_details = await self.host_profile_repo.get(user_id)
        if not profile_details:
            raise ValueError("No guide profile details available for the given user id")
        return profile_details