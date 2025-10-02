from app.api.schemas import KycSchema, KycResponseSchema, KycListResponseSchema, KycListItemSchema
from app.core.repositories import KycRepo
from app.core.enums import KycVerificationStatus
from app.core.use_cases import CloudinaryUseCase
import logging


logger = logging.getLogger(__name__)

class KycUseCase:
    def __init__(
            self,
            kyc_repo: KycRepo,        
    ):
        self.kyc_repo = kyc_repo

    #adding the kyc document from the user side
    async def add_or_update_kyc(self, user_id: str, kyc_data: KycSchema)->bool:
        existing_kyc = await self.kyc_repo.get(user_id)
        kyc_entity = kyc_data.to_entity()
        if not existing_kyc:
            return await self.kyc_repo.create(user_id=user_id, kyc_data= kyc_entity)

        if existing_kyc.verification_status == KycVerificationStatus.REJECTED:
            if existing_kyc.kyc_image_public_id:
                CloudinaryUseCase.delete_image(existing_kyc.kyc_image_public_id)
            return await self.kyc_repo.update_rejected(user_id=user_id, kyc_data = kyc_entity)
        
        raise ValueError("You already have an active KYC submission")    
    
    async def get_kyc(self, user_id: str)->KycResponseSchema | None:
        kyc_details = await self.kyc_repo.get(user_id)
        if not kyc_details:
            return None

        logger.info(f"I am inside the get_kyc and here is the kycentity: {kyc_details}")
        return KycResponseSchema(
            kycImageUrl=kyc_details.kyc_image_url,
            verificationStatus=kyc_details.verification_status,
            rejectionReason=kyc_details.rejection_reason
        )
    
    async def get_kyc_list(self, status: str, page: int = 1, limit: int = 10):
        skip = (page -1) * limit
        kyc_entities = await self.kyc_repo.get_kyc_list(status = status, skip=skip, limit=limit)
        total_count = await self.kyc_repo.get_kyc_count(status = status)

        kyc_schemas = [
            KycListItemSchema(
                userId = entity.user_id,
                email = entity.email,
                firstName = entity.first_name,
                lastName = entity.last_name,
                kycImageUrl = entity.kyc_image_url,
                verificationStatus = entity.verification_status,
                rejectionReason= entity.rejection_reason
            )
            for entity in kyc_entities
        ]

        return KycListResponseSchema(
            data=kyc_schemas,
            page = page,
            limit = limit,
            totalCount= total_count
        )
    
    async def accept_kyc(self, user_id:str)->bool:
        return await self.kyc_repo.accept_kyc(user_id = user_id)

    async def reject_kyc(self, user_id:str, rejection_reason: str)->bool:
        return await self.kyc_repo.reject_kyc(user_id = user_id, rejection_reason=rejection_reason)
    
    async def check_kyc_accepted(self, user_id: str)->bool:
        return await self.kyc_repo.check_kyc_accepted(user_id=user_id)