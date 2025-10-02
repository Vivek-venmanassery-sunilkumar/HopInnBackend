from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TravellerUserEntity(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    phone_number: Optional[str]
    dob: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class GuideUserEntity(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    phone_number: Optional[str]
    district: str
    country: str
    is_blocked: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class HostUserEntity(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    phone_number: Optional[str]
    is_blocked: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
