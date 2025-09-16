from pydantic import BaseModel

class GuideOnboardSchema(BaseModel):
    houseName: str
    country: str
    district: str
    state: str
    pincode: str
    coordinates: dict
    landmark: str
    about: str
    dob: str
    expertise: str
    knownLanguages: list
    profession: str
    hourlyRate: str