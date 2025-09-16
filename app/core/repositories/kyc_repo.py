from abc import ABC, abstractmethod
from app.core.entities import KycEntity, KycListItemEntity
from typing import List


class KycRepo(ABC):
    @abstractmethod
    async def create(self, user_id: str, kyc_data: KycEntity)->bool:
        pass

    @abstractmethod
    async def update_rejected(self, user_id:str, kyc_data: KycEntity)->bool:
        pass

    @abstractmethod
    async def check_kyc_exists(self, user_id:str)->bool:
        pass
    
    @abstractmethod
    async def get(self, user_id: str)->KycEntity | None:
        pass

    @abstractmethod
    async def get_kyc_list(self, status: str, skip: int = 0, limit: int = 10)->List[KycListItemEntity]:
        pass

    @abstractmethod
    async def get_kyc_count(self, status: str)->int:
        pass

    @abstractmethod
    async def accept_kyc(self, user_id: str)->bool:
        pass

    @abstractmethod
    async def reject_kyc(self, user_id: str, rejection_reason: str)->bool:
        pass

    @abstractmethod
    async def check_kyc_accepted(self, user_id:str)->bool:
        pass