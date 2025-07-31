from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    full_name: str
    email: str
    phone_number: str
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