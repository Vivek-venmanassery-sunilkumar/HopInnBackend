from abc import ABC, abstractmethod
from app.api.schemas import TravellerProfile


class TravellerProfileInterface(ABC):
    @abstractmethod
    async def get(user_id:str)->TravellerProfile:
        pass
