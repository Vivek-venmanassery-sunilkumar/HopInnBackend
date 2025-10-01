from pydantic import BaseModel, Field
from app.api.schemas.host.host import PropertyAddressSchema, PropertyImageSchema
from typing import List, Optional



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

class PropertyUpdateSchema(BaseModel):
    propertyName: Optional[str] = None
    propertyDescription: Optional[str] = None
    propertyType: Optional[str] = None
    maxGuests: Optional[int] = Field(None, gt=0, description="Must be greater than 0")
    bedrooms: Optional[int] = Field(None, gt=0, description="Must be greater than 0")
    pricePerNight: Optional[float] = Field(None, gt=0, description="Must be greater than 0")
    amenities: Optional[list] = None
    propertyAddress: Optional[PropertyAddressSchema] = None
    propertyImages: Optional[List[PropertyImageSchema]] = None
    property_id: str  # Required for identifying which property to update 

