from pydantic import BaseModel

class UserRolesAndPermissions(BaseModel):
    is_traveller: bool
    is_guide: bool
    is_host: bool
    is_admin: bool
    is_active: bool