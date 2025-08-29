from abc import ABC, abstractmethod
from app.api.schemas import TravellerProfileSchema


class TravellerProfileInterface(ABC):
    @abstractmethod
    async def get(user_id:str)->TravellerProfileSchema:
        pass

    @abstractmethod
    async def update_profile(self, user_id: str, update_data: dict)->bool:
        pass

    @abstractmethod
    async def get_public_id(self, user_id: str)->str | None:
        pass


    