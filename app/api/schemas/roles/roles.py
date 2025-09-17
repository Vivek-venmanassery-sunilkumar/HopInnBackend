from pydantic import BaseModel

class UserRolesSchema(BaseModel):
    id: str
    isActive: bool
    isTraveller: bool
    isGuide: bool
    isGuideBlocked: bool | None = None
    isAdmin: bool
    isHost: bool
    isHostBlocked: bool | None = None
    isKycVerified: bool | None = None

    class Config:
        from_attributes = True