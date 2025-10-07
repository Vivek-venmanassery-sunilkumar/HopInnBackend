from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
    
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

class PropertyDetailsWithTimestampsEntity(BaseModel):
    """Enhanced entity for property details with timestamps and host info"""
    property_id: str = Field(alias="propertyId")
    property_name: str = Field(alias="propertyName")
    property_description: str = Field(alias="propertyDescription")
    property_type: str = Field(alias="propertyType")
    max_guests: int = Field(..., gt=0, description="Must be greater than 0", alias="maxGuests")
    bedrooms: int = Field(..., gt=0, description="Must be greater than 0")
    price_per_night: float = Field(..., gt=0, description="Must be greater than 0", alias="pricePerNight")
    amenities: List[str]
    property_address: PropertyAddressEntity = Field(alias="propertyAddress")
    property_images: List[PropertyImageEntity] = Field(alias="propertyImages")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    host_id: int = Field(alias="hostId")

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


class PropertyUpdateEntity(BaseModel):
    """Entity for handling property updates with optional fields"""
    property_name: Optional[str] = Field(None, alias="propertyName")
    property_description: Optional[str] = Field(None, alias="propertyDescription")
    property_type: Optional[str] = Field(None, alias="propertyType")
    max_guests: Optional[int] = Field(None, gt=0, description="Must be greater than 0", alias="maxGuests")
    bedrooms: Optional[int] = Field(None, gt=0, description="Must be greater than 0")
    price_per_night: Optional[float] = Field(None, gt=0, description="Must be greater than 0", alias="pricePerNight")
    amenities: Optional[list] = None
    property_address: Optional[PropertyAddressEntity] = Field(None, alias="propertyAddress")
    property_images: Optional[List[PropertyImageEntity]] = Field(None, alias="propertyImages")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

    def get_update_data(self) -> dict:
        """Return only non-None fields for database update"""
        return self.model_dump(exclude_none=True, by_alias=False)

    def has_address_update(self) -> bool:
        """Check if address needs to be updated"""
        return self.property_address is not None

    def has_amenities_update(self) -> bool:
        """Check if amenities need to be updated"""
        return self.amenities is not None

    def has_images_update(self) -> bool:
        """Check if images need to be updated"""
        return self.property_images is not None

class HostEntity(BaseModel):
    about: str
    profession: str
    known_languages: list

class HostProfileUpdateEntity(BaseModel):
    """Entity for handling host profile updates with optional fields"""
    about: Optional[str] = None
    profession: Optional[str] = None
    known_languages: Optional[List[str]] = None

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

    def get_update_data(self) -> dict:
        """Return only non-None fields for database update"""
        return self.model_dump(exclude_none=True, by_alias=False)

    def has_about_update(self) -> bool:
        """Check if about field needs to be updated"""
        return self.about is not None

    def has_profession_update(self) -> bool:
        """Check if profession field needs to be updated"""
        return self.profession is not None

    def has_languages_update(self) -> bool:
        """Check if languages need to be updated"""
        return self.known_languages is not None
