from pydantic import BaseModel, Field

class GuideOnboardEntity(BaseModel):
    house_name: str = Field(alias="houseName")
    country: str
    district: str
    state: str
    pincode: str
    coordinates: dict
    landmark: str
    about: str
    expertise: str
    known_languages: list = Field(alias="knownLanguages")
    profession: str
    hourly_rate: str = Field(alias="hourlyRate")

    class Config:
        populate_by_name = True