from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
from app.core.entities.user_management_entity import TravellerUserEntity, GuideUserEntity, HostUserEntity


class UserManagementRepoInterface(ABC):
    @abstractmethod
    async def get_travellers(self) -> List[TravellerUserEntity]:
        pass

    @abstractmethod
    async def get_guides(self) -> List[GuideUserEntity]:
        pass

    @abstractmethod
    async def get_hosts(self) -> List[HostUserEntity]:
        pass

    @abstractmethod
    async def update_traveller_status(self, email: str, is_active: bool) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update_guide_status(self, email: str, is_blocked: bool) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update_host_status(self, email: str, is_blocked: bool) -> Dict[str, Any]:
        pass
