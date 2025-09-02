from pydantic import BaseModel, Field
from app.core.entities import KycEntity

class KycSchema(BaseModel):
    kycImageUrl: str = Field(..., alias='kyc_image_url')
    kycImagePublicId: str = Field(..., alias = 'kyc_image_public_id')

    class Config:
        populate_by_name = True
    
    def to_entity(self)->KycEntity:
        return KycEntity(**self.model_dump(by_alias=True))

class KycResponseSchema(BaseModel):
    kycImageUrl: str
    verificationStatus: str 
