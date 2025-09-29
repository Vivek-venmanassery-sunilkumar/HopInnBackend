from pydantic import BaseModel, Field
from app.api.schemas.host.host import PropertyAddressSchema, PropertyImageSchema
from typing import List



class PropertySchema(BaseModel):
    propertyName: str 
    propertyDescription: str 
    propertyType: str 
    maxGuests: int = Field(..., gt=0, description="Must be greater than 0")
    bedrooms: int = Field(..., gt=0, description="Must be greater than 0")
    pricePerNight: float = Field(..., gt=0, description="Must be greater than 0")
    amenities: list
    propertyAddress: PropertyAddressSchema 
    propertyImages: List[PropertyImageSchema] 

