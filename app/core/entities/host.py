from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
    
class PropertyAddressEntity(BaseModel):
    house_name: str = Field(alias="houseName")
    landmark: Optional[str] = None
    pincode: str
    district: str
    state: str
    country: str
    coordinates: dict

    model_config = ConfigDict(
        populate_by_name=True,  # This allows using field names too!
        from_attributes=True
    )

class PropertyImageEntity(BaseModel):
    image_url: str = Field(..., alias="imageUrl")
    is_primary: bool = Field(False, alias="isPrimary")
    public_id: Optional[str] = Field(None, alias="publicId")


    model_config = ConfigDict(
        populate_by_name=True,  # This allows using field names too!
        from_attributes=True
    )
class PropertyDetailsEntity(BaseModel):
    host_id: str
    property_name: str = Field(alias="propertyName")
    property_description: str = Field(alias="propertyDescription")
    property_type: str = Field(alias="propertyType")
    max_guests: int = Field(..., gt=0, description="Must be greater than 0", alias="maxGuests")
    bedrooms: int = Field(..., gt=0, description="Must be greater than 0")
    price_per_night: float = Field(..., gt=0, description="Must be greater than 0", alias="pricePerNight")
    amenities: list
    property_address: PropertyAddressEntity = Field(alias="propertyAddress")
    property_images: List[PropertyImageEntity] = Field(alias="propertyImages")

    model_config = ConfigDict(
        populate_by_name=True,  # This allows using field names too!
        from_attributes=True
    )

class PropertyOnlyDetailsEntity(BaseModel):
    property_id: str
    property_name: str = Field(alias="propertyName")
    property_description: str = Field(alias="propertyDescription")
    property_type: str = Field(alias="propertyType")
    max_guests: int = Field(..., gt=0, description="Must be greater than 0", alias="maxGuests")
    bedrooms: int = Field(..., gt=0, description="Must be greater than 0")
    price_per_night: float = Field(..., gt=0, description="Must be greater than 0", alias="pricePerNight")
    amenities: list
    property_address: PropertyAddressEntity = Field(alias="propertyAddress")
    property_images: List[PropertyImageEntity] = Field(alias="propertyImages")

    model_config = ConfigDict(
        populate_by_name=True,  # This allows using field names too!
        from_attributes=True
    )


class HostOnboardEntity(BaseModel):
    about: str
    profession: str
    known_languages: list = Field(alias="knownLanguages")
    property_name: str = Field(alias="propertyName")
    property_description: str = Field(alias="propertyDescription")
    property_type: str = Field(alias="propertyType")
    max_guests: int = Field(..., gt=0, description="Must be greater than 0", alias="maxGuests")
    bedrooms: int = Field(..., gt=0, description="Must be greater than 0")
    price_per_night: float = Field(..., gt=0, description="Must be greater than 0", alias="pricePerNight")
    amenities: list
    property_address: PropertyAddressEntity = Field(alias="propertyAddress")
    property_images: List[PropertyImageEntity] = Field(alias="propertyImages")


    model_config = {
        "populate_by_name": True
    }


class HostEntity(BaseModel):
    about: str
    profession: str
    known_languages: list
