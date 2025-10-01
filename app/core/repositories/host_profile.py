from abc import ABC, abstractmethod
from app.api.schemas import HostProfileSchema
from typing import Optional

class HostProfileInterface(ABC):
    @abstractmethod
    async def get(user_id: str)->Optional[HostProfileSchema]:
        pass