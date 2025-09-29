from app.core.repositories import PropertyRepo
from app.api.schemas import PropertySchema
from app.core.entities import PropertyDetailsEntity, PropertyOnlyDetailsEntity
from typing import List

class PropertyUseCase:
    def __init__(
            self,
            property_repo: PropertyRepo
    ):
        self.property_repo = property_repo
    
    async def add_property(self, user_id: str, property_data: PropertySchema)->str:
        host_id = await self.property_repo.get_host_id(user_id)
        property_dict = property_data.model_dump()
        property_details = PropertyDetailsEntity(
            host_id = str(host_id),
            **property_dict
        )

        return await self.property_repo.add_property(property_data=property_details)
    
    async def get_property(self, user_id: str)->List[PropertyOnlyDetailsEntity]:
        host_id = await self.property_repo.get_host_id(user_id)
        property_details = await self.property_repo.get_properties_by_host_id(host_id)
        return property_details



