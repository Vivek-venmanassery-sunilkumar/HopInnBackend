from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.admin_user_management import (
    TravellerEntity,
    GuideEntity,
    HostEntity,
    UserDetailsEntity,
)

class AdminUserManagementInterface(ABC):
    """Interface for admin user management repository operations"""
    
    @abstractmethod
    async def get_travellers(self) -> List[TravellerEntity]:
        """Get all travellers"""
        pass
    
    @abstractmethod
    async def get_guides(self) -> List[GuideEntity]:
        """Get all guides"""
        pass
    
    @abstractmethod
    async def get_hosts(self) -> List[HostEntity]:
        """Get all hosts"""
        pass
    
    @abstractmethod
    async def get_user_details(self, user_id: int) -> Optional[UserDetailsEntity]:
        """Get detailed user information by ID"""
        pass
    
    @abstractmethod
    async def deactivate_traveller(self, user_id: int) -> bool:
        """Deactivate traveller account"""
        pass
    
    @abstractmethod
    async def remove_host_privileges(self, user_id: int) -> bool:
        """Remove host privileges from user"""
        pass
    
    @abstractmethod
    async def remove_guide_privileges(self, user_id: int) -> bool:
        """Remove guide privileges from user"""
        pass
    
    
    @abstractmethod
    async def reactivate_traveller(self, user_id: int) -> bool:
        """Reactivate traveller account"""
        pass
    
    @abstractmethod
    async def reinstate_host_privileges(self, user_id: int) -> bool:
        """Reinstate host privileges for user"""
        pass
    
    @abstractmethod
    async def reinstate_guide_privileges(self, user_id: int) -> bool:
        """Reinstate guide privileges for user"""
        pass
