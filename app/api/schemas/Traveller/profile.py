from pydantic import BaseModel, field_validator
from datetime import date
from app.core.validations.types import StrictEmail
from typing import Optional



class TravellerProfileSchema(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[StrictEmail]
    phoneNumber: Optional[str]
    dob: Optional[date]
    profileImageUrl: Optional[str] = None
    profileImagePublicId: Optional[str] = None


class TravellerProfileUpdateSchema(BaseModel):
    firstName: str 
    lastName: str
    email: StrictEmail
    phoneNumber: str
    dob: date
    profileImageUrl: Optional[str] = None
    profileImagePublicId: Optional[str] = None

    @field_validator('dob', mode="before")
    def convert_string_to_date(cls, v):
        if isinstance(v, str):
            # Convert "YYYY-MM-DD" string to date object
            try:
                return date.fromisoformat(v)
            except (ValueError, TypeError):
                raise ValueError('Invalid date format. Expected YYYY-MM-DD')
        return v