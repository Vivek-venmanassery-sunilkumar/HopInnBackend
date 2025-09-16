from app.core.repositories import KycRepo, OnboardRepo
from app.core.entities import GuideOnboardEntity
from app.core.exceptions import KycNotAcceptedError
import logging


logger = logging.getLogger(__name__)


class OnBoardingUseCase:
    def __init__(
        self,
        kyc_repo: KycRepo,
        onboard_repo: OnboardRepo
    ):
        self.kyc_repo = kyc_repo
        self.onboard_repo = onboard_repo
    
    async def onboard_guide(self, data: GuideOnboardEntity, user_id: str)->bool:
        try:
            kyc_accepted = await self.kyc_repo.check_kyc_accepted(user_id)
            if not kyc_accepted:
                raise KycNotAcceptedError

            user_is_guide = await self.onboard_repo.user_is_guide(user_id)
            if user_is_guide:
                return True

            guide_onboarded = await self.onboard_repo.onboard_guide(data, user_id)

            if not guide_onboarded:
                return False
            updated = await self.onboard_repo.update_user_to_guide(user_id)
            return updated
        except KycNotAcceptedError:
            raise
        
        except Exception as e:
            logger.error(f"Error in guide onboarding for user {user_id}: {e}")
            return False