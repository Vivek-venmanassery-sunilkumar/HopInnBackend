from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    fullName: str
    email: str
    phoneNumber: str
    passwordHash: str
    profileImage: Optional[str] = None
    googleId: Optional[str] = None
    isAdmin: bool = False
    isGuide: bool = False
    isHost: bool = False
    isTraveller: bool = True
    isActive: bool = True
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True