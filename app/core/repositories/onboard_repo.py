from abc import ABC, abstractmethod
from app.core.entities import GuideOnboardEntity

class OnboardRepo(ABC):
    @abstractmethod
    async def onboard_guide(data:GuideOnboardEntity, user_id: str)->bool:
        pass

    @abstractmethod
    async def update_user_to_guide(user_id:str)->bool:
        pass

    @abstractmethod
    async def user_is_guide(user_id:str)->bool:
        pass