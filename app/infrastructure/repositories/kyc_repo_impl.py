from app.core.repositories import KycRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.entities import KycEntity
from app.infrastructure.database.models.users.user import UserKyc as KycModel
from sqlalchemy.future import select
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
import logging


logger = logging.getLogger(__name__)

class KycRepoImpl(KycRepo):
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
    
    async def add(self, user_id: str, kyc_data: KycEntity)->bool:
        try:
            db_model = KycModel(
                user_id= int(user_id),
                kyc_image_url = kyc_data.kyc_image_url,
                kyc_image_public_id=kyc_data.kyc_image_public_id
            )

            self.session.add(db_model)
            await self.session.commit()
            await self.session.refresh(db_model)
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to add KYC for user {user_id}: {e}")
            return False

    async def check_kyc_exists(self, user_id:str)->bool:
        result = await self.session.scalar(
           select(exists().where(KycModel.user_id == int(user_id)))
        )
        return result
    
    async def get(self, user_id: str)->KycEntity | None:
        kyc_data = await self.session.scalar(
            select(KycModel).where(KycModel.user_id == int(user_id))
        )

        if not kyc_data:
            return 
        
        return KycEntity(
            kyc_image_url=kyc_data.kyc_image_url,
            kyc_image_public_id=kyc_data.kyc_image_public_id,
            kyc_verification_status=kyc_data.verification_status
        )