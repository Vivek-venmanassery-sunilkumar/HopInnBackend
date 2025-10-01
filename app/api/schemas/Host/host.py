from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date



class PropertyAddressSchema(BaseModel):
    houseName: str
    landmark: Optional[str] = None
    pincode: str
    district: str
    state: str
    country: str
    coordinates: dict


class PropertyImageSchema(BaseModel):
    imageUrl: str
    isPrimary: bool = False
    publicId: Optional[str] = None


class HostOnboardSchema(BaseModel):
    about: str
    profession: str
    knownLanguages: List[str]
    propertyName: str
    propertyDescription: str
    propertyType: str
    maxGuests: int = Field(..., gt=0, description="Must be greater than 0")
    bedrooms: int = Field(..., gt=0, description="Must be greater than 0")
    pricePerNight: float = Field(..., gt=0, description="Must be greater than 0")
    amenities: List[str]
    propertyAddress: PropertyAddressSchema
    propertyImages: List[PropertyImageSchema]

class HostProfileSchema(BaseModel):
    about: str
    profession: str
    knownLanguages: List[str]
    joinedOn: date

class HostProfileUpdateSchema(BaseModel):
    about: Optional[str] = None
    profession: Optional[str] = None
    knownLanguages: Optional[List[str]] = None
