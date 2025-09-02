from pydantic import BaseModel
from typing import Optional


class KycEntity(BaseModel):
    kyc_image_url: str
    kyc_image_public_id: str
    verification_status: Optional[str] = "Pending"