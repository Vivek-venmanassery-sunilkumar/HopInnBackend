from abc import ABC, abstractmethod
from app.core.entities import KycEntity

class KycRepo(ABC):
    @abstractmethod
    async def add(self, user_id: str, kyc_data: KycEntity)->bool:
        pass

    @abstractmethod
    async def check_kyc_exists(self, user_id:str)->bool:
        pass
    
    @abstractmethod
    async def get(self, user_id: str)->KycEntity | None:
        pass