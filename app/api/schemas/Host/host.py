from pydantic import BaseModel, Field
from typing import Optional, List



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
    dob: str  
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