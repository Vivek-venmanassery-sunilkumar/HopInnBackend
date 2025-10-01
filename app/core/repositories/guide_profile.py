from abc import ABC, abstractmethod
from app.api.schemas import GuideProfileSchema
from app.core.entities import GuideOnboardEntity
from typing import Optional

class GuideProfileInterface(ABC):
    @abstractmethod
    async def get(user_id: str)->Optional[GuideProfileSchema]:
        pass

    @abstractmethod
    async def update_profile(user_id:str, guide_data:GuideOnboardEntity)->bool:
        pass