from app.api.schemas import KycSchema, KycResponseSchema
from app.core.repositories import KycRepo
import logging


logger = logging.getLogger(__name__)

class KycUseCase:
    def __init__(
            self,
            kyc_repo: KycRepo,        
    ):
        self.kyc_repo = kyc_repo

    async def add_kyc(self, user_id: str, kyc_data: KycSchema)->bool:
        result = await self.kyc_repo.check_kyc_exists(user_id)
        if result:
            raise ValueError("You have already uploaded the kyc documents.")
        
        kyc_entity = kyc_data.to_entity()
        
        success = await self.kyc_repo.add(user_id, kyc_entity)

        return success
    
    async def get_kyc(self, user_id: str)->KycResponseSchema | None:
        kyc_details = await self.kyc_repo.get(user_id)
        if not kyc_details:
            return None

        logger.info(f"I am inside the get_kyc and here is the kycentity: {kyc_details}")
        return KycResponseSchema(
            kycImageUrl=kyc_details.kyc_image_url,
            verificationStatus=kyc_details.verification_status
        )