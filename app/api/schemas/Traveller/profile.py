from pydantic import BaseModel
from app.core.validations.types import StrictEmail

class TravellerProfile(BaseModel):
    firstName: str
    lastName: str
    email: StrictEmail
    phoneNumber: str


