from app.core.repositories import GuideProfileInterface
from app.api.schemas import GuideProfileSchema

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