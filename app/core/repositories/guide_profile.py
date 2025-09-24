from abc import ABC, abstractmethod
from app.api.schemas import GuideProfileSchema
from typing import Optional

class GuideProfileInterface(ABC):
    @abstractmethod
    async def get(user_id: str)->Optional[GuideProfileSchema]:
        pass