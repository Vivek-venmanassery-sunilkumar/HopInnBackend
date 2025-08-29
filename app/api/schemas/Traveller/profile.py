from pydantic import BaseModel
from app.core.validations.types import StrictEmail
from typing import Optional



class TravellerProfileSchema(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[StrictEmail]
    phoneNumber: Optional[str]
    profileImageUrl: Optional[str] = None
    profileImagePublicId: Optional[str] = None

    