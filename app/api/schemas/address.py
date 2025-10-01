from pydantic import BaseModel
from typing import Optional

class AddressSchema(BaseModel):
    houseName: str
    landmark: Optional[str] = None
    pincode: str
    district: str
    state: str
    country: str
    coordinates: dict