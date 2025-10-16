from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Union
from decimal import Decimal
from datetime import datetime


class PropertySearchResponseSchema(BaseModel):
    """Schema for individual property in search results"""
    id: int
    propertyName: str
    propertyDescription: str
    childFriendly: bool
    maxGuests: int
    bedrooms: int
    pricePerNight: Decimal
    propertyType: str
    createdAt: datetime
    updatedAt: datetime
    hostId: int
    houseName: str
    landmark: Optional[str]
    pincode: str
    district: str
    state: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    primaryImageUrl: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "propertyName": "Cozy Beach House",
                "propertyDescription": "Beautiful beach house with ocean view",
                "maxGuests": 4,
                "bedrooms": 2,
                "pricePerNight": 150.00,
                "propertyType": "House",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
                "hostId": 1,
                "houseName": "Beach Villa",
                "landmark": "Near Beach",
                "pincode": "400001",
                "district": "Mumbai",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "primaryImageUrl": "https://res.cloudinary.com/example/image/upload/v1234567890/beach-house.jpg"
            }
        }


class PropertySearchResultSchema(BaseModel):
    """Schema for property search results response"""
    properties: List[PropertySearchResponseSchema]
    totalCount: int
    page: int
    pageSize: int
    message: str = "Properties found successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "properties": [],
                "totalCount": 0,
                "page": 1,
                "pageSize": 10,
                "message": "Properties found successfully"
            }
        }


class PropertySearchQueryParams(BaseModel):
    """Schema for property search query parameters from URL"""
    destination: Optional[str] = Field(None, description="Destination for search")
    guests: Optional[int] = Field(None, ge=1, description="Number of guests")
    fromDate: Optional[str] = Field(None, description="Check-in date")
    toDate: Optional[str] = Field(None, description="Check-out date")
    latitude: Optional[Union[str, float]] = Field(None, description="Latitude coordinate")
    longitude: Optional[Union[str, float]] = Field(None, description="Longitude coordinate")
    childrenOnboard: Optional[bool] = Field(None, description="Whether children are onboard for child-friendly prioritization")
    all: bool = Field(False, description="Get all properties without filtering")
    page: int = Field(1, ge=1, description="Page number for pagination")
    pageSize: int = Field(10, ge=1, le=100, description="Number of items per page")

    @field_validator('latitude', 'longitude', mode='before')
    @classmethod
    def validate_coordinates(cls, v):
        """Convert empty strings to None for latitude and longitude"""
        if v == "" or v is None:
            return None
        try:
            # Try to convert to float
            float_val = float(v)
            return float_val
        except (ValueError, TypeError):
            return None
    
    @field_validator('latitude')
    @classmethod
    def validate_latitude_range(cls, v):
        """Validate latitude range if not None"""
        if v is not None and isinstance(v, (int, float)) and (v < -90 or v > 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v
    
    @field_validator('longitude')
    @classmethod
    def validate_longitude_range(cls, v):
        """Validate longitude range if not None"""
        if v is not None and isinstance(v, (int, float)) and (v < -180 or v > 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v

    class Config:
        from_attributes = True

    def model_post_init(self, __context) -> None:
        """Custom validation after model initialization"""
        # If all=True, no validation needed
        if self.all:
            return
        
        # If all=False, validate required fields for property search
        if not self.destination or not self.destination.strip():
            raise ValueError("Destination is required when all=False")
        if self.guests is None or self.guests <= 0:
            raise ValueError("Guests must be a positive integer when all=False")


class GuideSearchResponseSchema(BaseModel):
    """Schema for individual guide in search results"""
    id: int
    userId: int
    bio: str
    profession: str
    expertise: str
    hourlyRate: str
    houseName: str
    landmark: Optional[str]
    pincode: str
    district: str
    state: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    createdAt: datetime
    updatedAt: datetime
    firstName: str
    lastName: Optional[str]
    profileImage: Optional[str]
    knownLanguages: List[str] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "userId": 1,
                "bio": "Experienced local guide with 5 years of experience",
                "profession": "Tour Guide",
                "expertise": "Historical sites, Food tours",
                "hourlyRate": "25.00",
                "houseName": "Guide House",
                "landmark": "Near City Center",
                "pincode": "400001",
                "district": "Mumbai",
                "state": "Maharashtra",
                "country": "India",
                "latitude": 19.0760,
                "longitude": 72.8777,
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
                "firstName": "John",
                "lastName": "Doe",
                "profileImage": "https://res.cloudinary.com/example/image/upload/v1234567890/profile.jpg",
                "knownLanguages": ["English", "Hindi", "Marathi"]
            }
        }


class GuideSearchResultSchema(BaseModel):
    """Schema for guide search results response"""
    guides: List[GuideSearchResponseSchema]
    totalCount: int
    page: int
    pageSize: int
    message: str = "Guides found successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "guides": [],
                "totalCount": 0,
                "page": 1,
                "pageSize": 10,
                "message": "Guides found successfully"
            }
        }


class GuideSearchQueryParams(BaseModel):
    """Schema for guide search query parameters from URL"""
    destination: Optional[str] = Field(None, description="Destination for search")
    latitude: Optional[Union[str, float]] = Field(None, description="Latitude coordinate")
    longitude: Optional[Union[str, float]] = Field(None, description="Longitude coordinate")
    childrenOnboard: Optional[bool] = Field(None, description="Whether children are onboard for child-friendly prioritization")
    all: bool = Field(False, description="Get all guides without filtering")
    page: int = Field(1, ge=1, description="Page number for pagination")
    pageSize: int = Field(10, ge=1, le=100, description="Number of items per page")

    @field_validator('latitude', 'longitude', mode='before')
    @classmethod
    def validate_coordinates(cls, v):
        """Convert empty strings to None for latitude and longitude"""
        if v == "" or v is None:
            return None
        try:
            # Try to convert to float
            float_val = float(v)
            return float_val
        except (ValueError, TypeError):
            return None
    
    @field_validator('latitude')
    @classmethod
    def validate_latitude_range(cls, v):
        """Validate latitude range if not None"""
        if v is not None and isinstance(v, (int, float)) and (v < -90 or v > 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v
    
    @field_validator('longitude')
    @classmethod
    def validate_longitude_range(cls, v):
        """Validate longitude range if not None"""
        if v is not None and isinstance(v, (int, float)) and (v < -180 or v > 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v

    class Config:
        from_attributes = True

    def model_post_init(self, __context) -> None:
        """Custom validation after model initialization"""
        # If all=True, no validation needed
        if self.all:
            return
        
        # If all=False, validate that we have either destination OR coordinates
        has_destination = self.destination and self.destination.strip()
        has_coordinates = self.latitude is not None and self.longitude is not None
        
        if not has_destination and not has_coordinates:
            raise ValueError("Either destination or coordinates must be provided when all=False")