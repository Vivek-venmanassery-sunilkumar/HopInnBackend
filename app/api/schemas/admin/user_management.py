from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserBasicInfo(BaseModel):
    """Basic user information for admin user management"""
    id: int
    firstName: str = Field(alias="first_name")
    lastName: str = Field(alias="last_name")
    email: str
    phoneNumber: Optional[str] = Field(None, alias="phone_number")
    isVerified: bool = Field(alias="is_verified")
    isActive: bool = Field(alias="is_active")
    joinedDate: datetime = Field(alias="created_at")
    lastActive: Optional[datetime] = Field(None, alias="last_login")
    profileImage: Optional[str] = Field(None, alias="profile_image_url")
    
    model_config = {"populate_by_name": True}

class TravellerInfo(UserBasicInfo):
    """Traveller specific information"""
    role: str = "traveller"
    status: str = Field(alias="status")
    
    model_config = {"populate_by_name": True}

class GuideInfo(UserBasicInfo):
    """Guide specific information"""
    role: str = "guide"
    status: str = Field(alias="status")
    isGuideBlocked: bool = Field(False, alias="is_guide_blocked")
    guideRating: Optional[float] = Field(None, alias="guide_rating")
    totalTours: int = Field(0, alias="total_tours")
    
    model_config = {"populate_by_name": True}

class HostInfo(UserBasicInfo):
    """Host specific information"""
    role: str = "host"
    status: str = Field(alias="status")
    isHostBlocked: bool = Field(False, alias="is_host_blocked")
    totalProperties: int = Field(0, alias="total_properties")
    hostRating: Optional[float] = Field(None, alias="host_rating")
    
    model_config = {"populate_by_name": True}

class UserDetails(BaseModel):
    """Detailed user information"""
    id: int
    firstName: str = Field(alias="first_name")
    lastName: str = Field(alias="last_name")
    email: str
    phoneNumber: Optional[str] = Field(None, alias="phone_number")
    isVerified: bool = Field(alias="is_verified")
    isActive: bool = Field(alias="is_active")
    joinedDate: datetime = Field(alias="created_at")
    lastActive: Optional[datetime] = Field(None, alias="last_login")
    profileImage: Optional[str] = Field(None, alias="profile_image_url")
    roles: List[str] = []
    isAdmin: bool = Field(False, alias="is_admin")
    isHost: bool = Field(False, alias="is_host")
    isGuide: bool = Field(False, alias="is_guide")
    isTraveller: bool = Field(False, alias="is_traveller")
    isHostBlocked: bool = Field(False, alias="is_host_blocked")
    isGuideBlocked: bool = Field(False, alias="is_guide_blocked")
    
    model_config = {"populate_by_name": True}

class UserListResponse(BaseModel):
    """Response for user list endpoints"""
    success: bool
    message: str
    users: List[UserBasicInfo]
    total_count: int
    
    model_config = {"populate_by_name": True}

class UserDetailsResponse(BaseModel):
    """Response for user details endpoint"""
    success: bool
    message: str
    user: UserDetails
    
    model_config = {"populate_by_name": True}


class UserActionResponse(BaseModel):
    """Response for user action endpoints"""
    success: bool
    message: str
    
    model_config = {"populate_by_name": True}
