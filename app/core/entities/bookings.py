from pydantic import BaseModel, field_validator, Field
from datetime import date


class PropertyBookingsCheckEntity(BaseModel):
    property_id: int = Field(alias='propertyId')
    num_children: int = Field(default=0, alias='numChildren')
    num_adults: int = Field(alias='numAdults')
    num_infants: int = Field(default=0, alias='numInfants')
    check_in_date: date = Field(alias='checkInDate')
    check_out_date: date = Field(alias='checkOutDate')
    total_guests: int = Field(default=0, alias='totalGuests')

    @field_validator('total_guests', mode='before')
    @classmethod
    def calculate_total_guests(cls, v, values):
        """Calculate total_guests as the sum of num_adults and num_children"""
        if 'num_adults' in values and 'num_children' in values:
            return values['num_adults'] + values['num_children']
        return v

    @field_validator('num_adults', 'num_children', 'num_infants')
    @classmethod
    def validate_guest_counts(cls, v):
        """Validate that guest counts are non-negative"""
        if v < 0:
            raise ValueError('Guest counts must be non-negative')
        return v

    @field_validator('num_adults')
    @classmethod
    def validate_adults_minimum(cls, v):
        """Validate that there is at least one adult"""
        if v < 1:
            raise ValueError('At least one adult is required')
        return v

    class Config:
        populate_by_name = True  # Allow both alias and field name
        json_encoders = {
            date: lambda v: v.isoformat()
        }