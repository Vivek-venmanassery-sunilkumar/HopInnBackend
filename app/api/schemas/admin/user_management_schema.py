from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class TravellerUserSchema(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    firstName: str
    lastName: Optional[str]
    email: str
    phoneNumber: Optional[str]
    dob: Optional[str]
    isActive: bool
    createdAt: datetime


class GuideUserSchema(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    firstName: str
    lastName: Optional[str]
    email: str
    phoneNumber: Optional[str]
    district: str
    country: str
    isBlocked: bool
    isActive: bool
    createdAt: datetime


class HostUserSchema(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    firstName: str
    lastName: Optional[str]
    email: str
    phoneNumber: Optional[str]
    isBlocked: bool
    isActive: bool
    createdAt: datetime


class UserStatusUpdateRequestSchema(BaseModel):
    email: str
    is_active: Optional[bool] = None
    is_blocked: Optional[bool] = None


class UserStatusUpdateResponseSchema(BaseModel):
    message: str
    data: dict
