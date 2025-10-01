from pydantic import BaseModel

class UserRolesAndPermissionsEntity(BaseModel):
    is_traveller: bool
    is_guide: bool
    is_guide_blocked: bool | None = None
    is_host_blocked: bool | None = None
    is_host: bool
    is_admin: bool
    is_active: bool