from app.core.repositories import KycRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.entities import KycEntity, KycListItemEntity
from app.core.enums import KycVerificationStatus
from app.infrastructure.database.models.users.user import UserKyc as KycModel, User
from sqlalchemy.future import select
from sqlalchemy import exists, func
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging



logger = logging.getLogger(__name__)

class KycRepoImpl(KycRepo):
    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
    
    #adding the kyc details from the user side
    async def create(self, user_id: str, kyc_data: KycEntity)->bool:
        try:
            db_model = KycModel(
                user_id= int(user_id),
                kyc_image_url = kyc_data.kyc_image_url,
                kyc_image_public_id=kyc_data.kyc_image_public_id,
                rejection_reason = None,
                verification_status = kyc_data.verification_status.value
            )

            self.session.add(db_model)
            await self.session.commit()
            await self.session.refresh(db_model)
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to add KYC for user {user_id}: {e}")
            return False

    async def update_rejected(self, user_id: str, kyc_data: KycEntity)->bool:
        try:
            result = await self.session.execute(
                select(KycModel)
                .where(
                    KycModel.user_id == int(user_id)
                )
            )
            kyc = result.scalar_one_or_none()
            if not kyc:
                return False
            
            kyc.kyc_image_url =kyc_data.kyc_image_url
            kyc.kyc_image_public_id = kyc_data.kyc_image_public_id
            kyc.verification_status = KycVerificationStatus.PENDING.value
            kyc.rejection_reason = None

            await self.session.commit()
            await self.session.refresh(kyc)
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to update rejected KYC for user {user_id}: {e}")
            return False
            
    #checking if kyc data exists in the user side
    async def check_kyc_exists(self, user_id:str)->bool:
        result = await self.session.scalar(
           select(exists().where(KycModel.user_id == int(user_id)))
        )
        return result
    
    #checking if kyc data exists and is accepted
    async def check_kyc_accepted(self, user_id:str)->bool:
        kyc_data = await self.get(user_id=user_id)
        if not kyc_data:
            return False
        
        if kyc_data.verification_status != KycVerificationStatus.ACCEPTED:
            return False
        
        return True

        
    
    #getting the kyc data for a particular user
    async def get(self, user_id: str)->KycEntity | None:
        kyc_data = await self.session.scalar(
            select(KycModel).where(KycModel.user_id == int(user_id))
        )

        if not kyc_data:
            return 
        
        return KycEntity(
            kyc_image_url=kyc_data.kyc_image_url,
            kyc_image_public_id=kyc_data.kyc_image_public_id,
            verification_status=(KycVerificationStatus(kyc_data.verification_status)),
            rejection_reason= kyc_data.rejection_reason
        )

    #getting the kyc data according to the verification status in a paginated manner 
    async def get_kyc_list(self, status: str, skip: int= 0, limit: int = 10)->List[KycListItemEntity]:
        result = await self.session.execute(
            select(KycModel, User)
            .join(User, KycModel.user_id == User.id)
            .where(KycModel.verification_status == status)
            .offset(skip)
            .limit(limit)
        )
        logger.info(type(result))

        logger.info(f'the data inside execute: {result}')

        kyc_list_items = result.all()

        return [
            KycListItemEntity(
                user_id=str(item[0].user_id),
                email=item[1].email,
                first_name=item[1].first_name,
                last_name=item[1].last_name,
                kyc_image_url=item[0].kyc_image_url,
                verification_status=KycVerificationStatus(item[0].verification_status),
                rejection_reason=item[0].rejection_reason
            )
            for item in kyc_list_items
        ]

    #getting the total count of the kyc documents 
    async def get_kyc_count(self, status: str)->int:
        result = await self.session.execute(
            select(func.count(KycModel.id))
            .where(KycModel.verification_status==status)
        )

        return result.scalar() or 0

    async def accept_kyc(self, user_id: str)->bool:
        result = await self.session.execute(
            select(KycModel).where(KycModel.user_id == int(user_id))
        )

        kyc = result.scalar_one_or_none()

        if not kyc:
            raise ValueError("KYC record not found")

        kyc.verification_status = KycVerificationStatus.ACCEPTED.value
        await self.session.commit()
        await self.session.refresh(kyc)

        return True
    
    async def reject_kyc(self, user_id: str, rejection_reason: str)->bool:
        result = await self.session.execute(
            select(KycModel).where(KycModel.user_id == int(user_id))
        )

        kyc = result.scalar_one_or_none()
        if not kyc:
            raise ValueError("KYC record not found")
        
        kyc.verification_status = KycVerificationStatus.REJECTED.value
        kyc.rejection_reason = rejection_reason
        await self.session.commit()
        await self.session.refresh(kyc)
        
        return True
    
    