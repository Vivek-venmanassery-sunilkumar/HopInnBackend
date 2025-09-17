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
    dob: str
    expertise: str
    known_languages: list = Field(alias="knownLanguages")
    profession: str
    hourly_rate: str = Field(alias="hourlyRate")

    class config:
        allow_population_by_field_name = True
