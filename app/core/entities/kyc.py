from pydantic import BaseModel
from typing import Optional
from app.core.enums import KycVerificationStatus

class KycEntity(BaseModel):
    kyc_image_url: str
    kyc_image_public_id: str
    verification_status: KycVerificationStatus = KycVerificationStatus.PENDING
    rejection_reason: Optional[str] = None

class KycListItemEntity(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: Optional[str] = None
    kyc_image_url: str
    verification_status: KycVerificationStatus
    rejection_reason: Optional[str] = None