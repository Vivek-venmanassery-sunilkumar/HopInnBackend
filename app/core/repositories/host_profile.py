from abc import ABC, abstractmethod
from app.api.schemas import HostProfileSchema
from app.core.entities import HostProfileUpdateEntity
from typing import Optional

class HostProfileInterface(ABC):
    @abstractmethod
    async def get(user_id: str)->Optional[HostProfileSchema]:
        pass

    @abstractmethod
    async def update_profile(self, user_id: str, update_data: HostProfileUpdateEntity)->bool:
        pass