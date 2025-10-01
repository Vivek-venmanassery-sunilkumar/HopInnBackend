from typing import List, Optional
from app.core.repositories.admin_user_management import AdminUserManagementInterface
from app.core.entities.admin_user_management import (
    TravellerEntity,
    GuideEntity,
    HostEntity,
    UserDetailsEntity
)
from app.api.schemas.admin.user_management import (
    TravellerInfo,
    GuideInfo,
    HostInfo,
    UserDetails
)
import logging

logger = logging.getLogger(__name__)

class AdminUserManagementUseCase:
    """Use case for admin user management operations"""
    
    def __init__(self, admin_user_repo: AdminUserManagementInterface):
        self.admin_user_repo = admin_user_repo
    
    async def get_travellers(self) -> List[TravellerInfo]:
        """Get all travellers"""
        try:
            travellers = await self.admin_user_repo.get_travellers()
            
            # Convert snake_case entities to camelCase schemas
            traveller_schemas = [
                TravellerInfo(
                    id=t.id,
                    firstName=t.first_name,
                    lastName=t.last_name,
                    email=t.email,
                    phoneNumber=t.phone_number,
                    isVerified=t.is_verified,
                    isActive=t.is_active,
                    joinedDate=t.created_at,
                    lastActive=t.last_login,
                    profileImage=t.profile_image_url,
                    status=t.status
                ) for t in travellers
            ]
            
            logger.info(f"Retrieved {len(traveller_schemas)} travellers")
            return traveller_schemas
        except Exception as e:
            logger.error(f"Error getting travellers: {str(e)}")
            raise
    
    async def get_guides(self) -> List[GuideInfo]:
        """Get all guides"""
        try:
            guides = await self.admin_user_repo.get_guides()
            
            # Convert snake_case entities to camelCase schemas
            guide_schemas = [
                GuideInfo(
                    id=g.id,
                    firstName=g.first_name,
                    lastName=g.last_name,
                    email=g.email,
                    phoneNumber=g.phone_number,
                    isVerified=g.is_verified,
                    isActive=g.is_active,
                    joinedDate=g.created_at,
                    lastActive=g.last_login,
                    profileImage=g.profile_image_url,
                    status=g.status,
                    isGuideBlocked=g.is_guide_blocked,
                    guideRating=g.guide_rating,
                    totalTours=g.total_tours
                ) for g in guides
            ]
            
            logger.info(f"Retrieved {len(guide_schemas)} guides")
            return guide_schemas
        except Exception as e:
            logger.error(f"Error getting guides: {str(e)}")
            raise
    
    async def get_hosts(self) -> List[HostInfo]:
        """Get all hosts"""
        try:
            hosts = await self.admin_user_repo.get_hosts()
            
            # Convert snake_case entities to camelCase schemas
            host_schemas = [
                HostInfo(
                    id=h.id,
                    firstName=h.first_name,
                    lastName=h.last_name,
                    email=h.email,
                    phoneNumber=h.phone_number,
                    isVerified=h.is_verified,
                    isActive=h.is_active,
                    joinedDate=h.created_at,
                    lastActive=h.last_login,
                    profileImage=h.profile_image_url,
                    status=h.status,
                    isHostBlocked=h.is_host_blocked,
                    totalProperties=h.total_properties,
                    hostRating=h.host_rating
                ) for h in hosts
            ]
            
            logger.info(f"Retrieved {len(host_schemas)} hosts")
            return host_schemas
        except Exception as e:
            logger.error(f"Error getting hosts: {str(e)}")
            raise
    
    async def get_user_details(self, user_id: int) -> Optional[UserDetails]:
        """Get detailed user information"""
        try:
            user = await self.admin_user_repo.get_user_details(user_id)
            if user:
                # Convert snake_case entity to camelCase schema
                user_schema = UserDetails(
                    id=user.id,
                    firstName=user.first_name,
                    lastName=user.last_name,
                    email=user.email,
                    phoneNumber=user.phone_number,
                    isVerified=user.is_verified,
                    isActive=user.is_active,
                    joinedDate=user.created_at,
                    lastActive=user.last_login,
                    profileImage=user.profile_image_url,
                    roles=user.roles,
                    isAdmin=user.is_admin,
                    isHost=user.is_host,
                    isGuide=user.is_guide,
                    isTraveller=user.is_traveller,
                    isHostBlocked=user.is_host_blocked,
                    isGuideBlocked=user.is_guide_blocked
                )
                logger.info(f"Retrieved user details for user {user_id}")
                return user_schema
            else:
                logger.warning(f"User {user_id} not found")
                return None
        except Exception as e:
            logger.error(f"Error getting user details for user {user_id}: {str(e)}")
            raise
    
    async def deactivate_traveller(self, user_id: int) -> bool:
        """Deactivate traveller account"""
        try:
            success = await self.admin_user_repo.deactivate_traveller(user_id)
            if success:
                logger.info(f"Successfully deactivated traveller {user_id}")
            else:
                logger.warning(f"Failed to deactivate traveller {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error deactivating traveller {user_id}: {str(e)}")
            raise
    
    async def remove_host_privileges(self, user_id: int) -> bool:
        """Remove host privileges from user"""
        try:
            success = await self.admin_user_repo.remove_host_privileges(user_id)
            if success:
                logger.info(f"Successfully removed host privileges for user {user_id}")
            else:
                logger.warning(f"Failed to remove host privileges for user {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error removing host privileges for user {user_id}: {str(e)}")
            raise
    
    async def remove_guide_privileges(self, user_id: int) -> bool:
        """Remove guide privileges from user"""
        try:
            success = await self.admin_user_repo.remove_guide_privileges(user_id)
            if success:
                logger.info(f"Successfully removed guide privileges for user {user_id}")
            else:
                logger.warning(f"Failed to remove guide privileges for user {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error removing guide privileges for user {user_id}: {str(e)}")
            raise
    
    
    async def reactivate_traveller(self, user_id: int) -> bool:
        """Reactivate traveller account"""
        try:
            success = await self.admin_user_repo.reactivate_traveller(user_id)
            if success:
                logger.info(f"Successfully reactivated traveller {user_id}")
            else:
                logger.warning(f"Failed to reactivate traveller {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error reactivating traveller {user_id}: {str(e)}")
            raise
    
    async def reinstate_host_privileges(self, user_id: int) -> bool:
        """Reinstate host privileges for user"""
        try:
            success = await self.admin_user_repo.reinstate_host_privileges(user_id)
            if success:
                logger.info(f"Successfully reinstated host privileges for user {user_id}")
            else:
                logger.warning(f"Failed to reinstate host privileges for user {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error reinstating host privileges for user {user_id}: {str(e)}")
            raise
    
    async def reinstate_guide_privileges(self, user_id: int) -> bool:
        """Reinstate guide privileges for user"""
        try:
            success = await self.admin_user_repo.reinstate_guide_privileges(user_id)
            if success:
                logger.info(f"Successfully reinstated guide privileges for user {user_id}")
            else:
                logger.warning(f"Failed to reinstate guide privileges for user {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error reinstating guide privileges for user {user_id}: {str(e)}")
            raise
