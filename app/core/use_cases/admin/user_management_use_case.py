from typing import List, Union, Dict, Any
from app.core.repositories.user_management_repo_interface import UserManagementRepoInterface
from app.core.entities.user_management_entity import TravellerUserEntity, GuideUserEntity, HostUserEntity
from app.api.schemas.admin.user_management_schema import TravellerUserSchema, GuideUserSchema, HostUserSchema


class UserManagementUseCase:
    def __init__(self, user_management_repo: UserManagementRepoInterface):
        self.user_management_repo = user_management_repo

    async def get_users_by_role(self, role: str) -> List[Union[TravellerUserSchema, GuideUserSchema, HostUserSchema]]:
        if role == "traveller":
            entities = await self.user_management_repo.get_travellers()
            return [
                TravellerUserSchema(
                    firstName=entity.first_name,
                    lastName=entity.last_name,
                    email=entity.email,
                    phoneNumber=entity.phone_number,
                    dob=entity.dob,
                    isActive=entity.is_active,
                    createdAt=entity.created_at
                )
                for entity in entities
            ]
        
        elif role == "guide":
            entities = await self.user_management_repo.get_guides()
            return [
                GuideUserSchema(
                    firstName=entity.first_name,
                    lastName=entity.last_name,
                    email=entity.email,
                    phoneNumber=entity.phone_number,
                    district=entity.district,
                    country=entity.country,
                    isBlocked=entity.is_blocked,
                    isActive=entity.is_active,
                    createdAt=entity.created_at
                )
                for entity in entities
            ]
        
        elif role == "host":
            entities = await self.user_management_repo.get_hosts()
            return [
                HostUserSchema(
                    firstName=entity.first_name,
                    lastName=entity.last_name,
                    email=entity.email,
                    phoneNumber=entity.phone_number,
                    isBlocked=entity.is_blocked,
                    isActive=entity.is_active,
                    createdAt=entity.created_at
                )
                for entity in entities
            ]
        
        else:
            raise ValueError(f"Invalid role: {role}. Role must be 'traveller', 'guide', or 'host'")

    async def update_traveller_status(self, email: str, is_active: bool) -> Dict[str, Any]:
        """
        Update traveller status (is_active in User model)
        If blocking traveller, also block their guide and host privileges
        """
        return await self.user_management_repo.update_traveller_status(email, is_active)

    async def update_guide_status(self, email: str, is_blocked: bool) -> Dict[str, Any]:
        """
        Update guide status (is_blocked in Guide model)
        """
        return await self.user_management_repo.update_guide_status(email, is_blocked)

    async def update_host_status(self, email: str, is_blocked: bool) -> Dict[str, Any]:
        """
        Update host status (is_blocked in Host model)
        """
        return await self.user_management_repo.update_host_status(email, is_blocked)
