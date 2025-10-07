from abc import ABC, abstractmethod
from app.core.entities import PropertyDetailsEntity, PropertyOnlyDetailsEntity, PropertyUpdateEntity, PropertyDetailsWithTimestampsEntity
from typing import List, Optional

class PropertyRepo(ABC):
    @abstractmethod
    async def add_property(self, property_data: PropertyDetailsEntity)->str | None:
        pass

    @abstractmethod
    async def get_host_id(self, user_id: str)->str:
        pass

    @abstractmethod
    async def get_properties_by_host_id(self, host_id: int)->List[PropertyOnlyDetailsEntity]:
        pass

    @abstractmethod
    async def get_property_by_id(self, property_id: int)->Optional[PropertyOnlyDetailsEntity]:
        pass

    @abstractmethod
    async def get_property_details_by_id(self, property_id: int)->Optional[PropertyDetailsWithTimestampsEntity]:
        pass

    @abstractmethod
    async def update_property(self, property_id: str, property_data: PropertyUpdateEntity, host_id: int)->bool:
        pass