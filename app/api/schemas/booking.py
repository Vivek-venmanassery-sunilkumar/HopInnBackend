from pydantic import BaseModel, field_validator
from datetime import date

class PropertyBookingsCheckSchema(BaseModel):
    propertyId: int
    numChildren: int = 0
    numAdults: int
    numInfants: int = 0
    checkInDate: date
    checkOutDate: date
    totalGuests: int = 0

    @field_validator('totalGuests', mode='before')
    @classmethod
    def calculate_total_guests(cls, v, values):
        """Calculate totalGuests as the sum of numAdults and numChildren"""
        if 'numAdults' in values and 'numChildren' in values:
            return values['numAdults'] + values['numChildren']
        return v

    @field_validator('numAdults', 'numChildren', 'numInfants')
    @classmethod
    def validate_guest_counts(cls, v):
        """Validate that guest counts are non-negative"""
        if v < 0:
            raise ValueError('Guest counts must be non-negative')
        return v

    @field_validator('numAdults')
    @classmethod
    def validate_adults_minimum(cls, v):
        """Validate that there is at least one adult"""
        if v < 1:
            raise ValueError('At least one adult is required')
        return v
