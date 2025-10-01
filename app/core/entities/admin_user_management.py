from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AdminUserEntity(BaseModel):
    """Base entity for admin user management"""
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    is_verified: bool = False
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None
    profile_image_url: Optional[str] = None
    
    model_config = {"from_attributes": True}

class TravellerEntity(AdminUserEntity):
    """Traveller entity for admin management"""
    role: str = "traveller"
    status: str = "active"

class GuideEntity(AdminUserEntity):
    """Guide entity for admin management"""
    role: str = "guide"
    status: str = "active"
    is_guide_blocked: bool = False
    guide_rating: Optional[float] = None
    total_tours: int = 0

class HostEntity(AdminUserEntity):
    """Host entity for admin management"""
    role: str = "host"
    status: str = "active"
    is_host_blocked: bool = False
    total_properties: int = 0
    host_rating: Optional[float] = None

class UserDetailsEntity(AdminUserEntity):
    """Detailed user entity for admin management"""
    roles: List[str] = []
    is_admin: bool = False
    is_host: bool = False
    is_guide: bool = False
    is_traveller: bool = False
    is_host_blocked: bool = False
    is_guide_blocked: bool = False

