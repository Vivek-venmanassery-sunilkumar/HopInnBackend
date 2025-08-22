from pydantic import BaseModel
from app.core.validations.types import StrictEmail
from typing import Optional

class TravellerProfile(BaseModel):
    firstName: str
    lastName: Optional[str]
    email: StrictEmail
    phoneNumber: str


