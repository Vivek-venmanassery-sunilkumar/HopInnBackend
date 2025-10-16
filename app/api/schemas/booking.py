from pydantic import BaseModel, field_validator, model_validator
from datetime import date

class PropertyBookingsCheckSchema(BaseModel):
    propertyId: int
    numChildren: int = 0
    numAdults: int
    numInfants: int = 0
    checkInDate: date
    checkOutDate: date
    totalGuests: int = 0

    @model_validator(mode='after')
    def calculate_total_guests(self):
        """Calculate totalGuests as the sum of numAdults and numChildren"""
        self.totalGuests = self.numAdults + self.numChildren
        return self

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

class GuestsSchema(BaseModel):
    numAdults: int
    numChildren: int
    numInfants: int
    propertyId: int
    checkInDate: date
    checkOutDate: date
    totalGuests: int
