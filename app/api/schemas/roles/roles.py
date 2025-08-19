from pydantic import BaseModel

class UserRoles(BaseModel):
    id: str
    isActive: bool
    isTraveller: bool
    isGuide: bool
    isAdmin: bool
    isHost: bool

    class Config:
        from_attributes = True