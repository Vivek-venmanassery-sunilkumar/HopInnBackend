from pydantic import BaseModel, Field
from typing import Optional
from app.core.validations.types import StrictEmail
from datetime import date


class TravellerUpdateProfileEntity(BaseModel):
    first_name: Optional[str]=Field(alias='firstName')
    last_name: Optional[str]=Field(alias='lastName')
    email: Optional[StrictEmail]
    dob: Optional[date]
    phone_number: Optional[str]=Field(alias='phoneNumber')
    profile_image_public_id: Optional[str]=Field(alias="profileImagePublicId")
    profile_image: Optional[str] = Field(alias="profileImageUrl")