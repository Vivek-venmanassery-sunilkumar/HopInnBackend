from pydantic import BaseModel
from app.api.schemas.address import AddressSchema
from datetime import date
from typing import Optional

class GuideOnboardSchema(BaseModel):
    houseName: str
    country: str
    district: str
    state: str
    pincode: str
    coordinates: dict
    landmark: Optional[str]
    about: str
    expertise: str
    knownLanguages: list
    profession: str
    hourlyRate: str

class GuideProfileSchema(BaseModel):
    bio: str
    profession: str
    hourly_rate: str
    expertise: str
    address: AddressSchema
    knownLanguages: list
    joinedOn: date
