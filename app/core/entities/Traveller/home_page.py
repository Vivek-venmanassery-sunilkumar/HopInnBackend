from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class PropertySearchEntity(BaseModel):
    """Entity for property search results"""
    id: int
    property_name: str
    property_description: str
    child_friendly: bool
    max_guests: int
    bedrooms: int
    price_per_night: Decimal
    property_type: str
    created_at: datetime
    updated_at: datetime
    host_id: int
    house_name: str
    landmark: Optional[str]
    pincode: str
    district: str
    state: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    primary_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class PropertySearchQueryEntity(BaseModel):
    """Entity for property search query parameters"""
    destination: Optional[str] = None
    guests: Optional[int] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    all: bool = False  # New parameter to get all properties
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    class Config:
        from_attributes = True


class PropertySearchResultEntity(BaseModel):
    """Entity for property search results response"""
    properties: List[PropertySearchEntity]
    total_count: int
    page: int
    page_size: int

    class Config:
        from_attributes = True


class GuideSearchEntity(BaseModel):
    """Entity for guide search results"""
    id: int
    user_id: int
    bio: str
    profession: str
    expertise: str
    hourly_rate: str
    house_name: str
    landmark: Optional[str]
    pincode: str
    district: str
    state: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime
    updated_at: datetime
    first_name: str
    last_name: Optional[str]
    profile_image: Optional[str]
    known_languages: List[str] = []

    class Config:
        from_attributes = True


class GuideSearchQueryEntity(BaseModel):
    """Entity for guide search query parameters"""
    destination: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    all: bool = False  # New parameter to get all guides
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    class Config:
        from_attributes = True


class GuideSearchResultEntity(BaseModel):
    """Entity for guide search results response"""
    guides: List[GuideSearchEntity]
    total_count: int
    page: int
    page_size: int

    class Config:
        from_attributes = True