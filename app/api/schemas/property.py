from pydantic import BaseModel, Field
from app.api.schemas.host.host import PropertyAddressSchema, PropertyImageSchema
from typing import List, Optional
from datetime import datetime



class PropertySchema(BaseModel):
    propertyName: str 
    propertyDescription: str 
    propertyType: str 
    maxGuests: int = Field(..., gt=0, description="Must be greater than 0")
    bedrooms: int = Field(..., gt=0, description="Must be greater than 0")
    pricePerNight: float = Field(..., gt=0, description="Must be greater than 0")
    amenities: List[str]
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

class PropertyDetailsResponseSchema(BaseModel):
    """Schema for property details response"""
    propertyId: str
    propertyName: str
    propertyDescription: str
    propertyType: str
    maxGuests: int
    bedrooms: int
    pricePerNight: float
    amenities: List[str]
    propertyAddress: PropertyAddressSchema
    propertyImages: List[PropertyImageSchema]
    createdAt: datetime
    updatedAt: datetime
    hostId: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "propertyId": "1",
                "propertyName": "Cozy Beach House",
                "propertyDescription": "Beautiful beach house with ocean view",
                "propertyType": "House",
                "maxGuests": 4,
                "bedrooms": 2,
                "pricePerNight": 150.00,
                "amenities": ["WiFi", "Parking", "Kitchen", "Pool"],
                "propertyAddress": {
                    "houseName": "Beach Villa",
                    "landmark": "Near Beach",
                    "pincode": "400001",
                    "district": "Mumbai",
                    "state": "Maharashtra",
                    "country": "India",
                    "coordinates": {
                        "latitude": 19.0760,
                        "longitude": 72.8777
                    }
                },
                "propertyImages": [
                    {
                        "imageUrl": "https://res.cloudinary.com/example/image/upload/v1234567890/beach-house.jpg",
                        "isPrimary": True,
                        "publicId": "beach-house-1"
                    }
                ],
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
                "hostId": 1
            }
        }

