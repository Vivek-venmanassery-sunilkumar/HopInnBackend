from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserEntity(BaseModel):
    id: Optional[str] = None
    first_name: str = None
    last_name: str
    email: str
    phone_number: Optional[str] = None
    password_hash: str
    profile_image: Optional[str] = None
    google_id: Optional[str] = None
    is_admin: bool = False
    is_guide: bool = False
    is_host: bool = False
    is_traveller: bool = True
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdminCreationEntity(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str
    phone_number: str = None
    password: str
    is_admin: bool = True
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None