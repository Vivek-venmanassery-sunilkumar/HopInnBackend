from pydantic import BaseModel, Field
from app.core.entities import KycEntity
from typing import List, Optional
from app.core.enums import KycVerificationStatus

class KycSchema(BaseModel):
    kycImageUrl: str = Field(..., alias='kyc_image_url')
    kycImagePublicId: str = Field(..., alias = 'kyc_image_public_id')

    class Config:
        populate_by_name = True
    
    def to_entity(self)->KycEntity:
        return KycEntity(**self.model_dump(by_alias=True))

class KycResponseSchema(BaseModel):
    kycImageUrl: str
    verificationStatus: KycVerificationStatus 
    rejectionReason: Optional[str] = None

class KycListItemSchema(BaseModel):
    userId: str
    kycImageUrl: str
    verificationStatus: KycVerificationStatus
    rejectionReason: Optional[str] = None

class KycListResponseSchema(BaseModel):
    success: bool = True
    message: str = 'KYC data retrieved successfully'
    data: List[KycListItemSchema]
    limit: int
    page: int
    totalCount: int


class KycAcceptRequestSchema(BaseModel):
    userId: str

class KycRejectRequestSchema(BaseModel):
    userId: str
    rejectionReason:str