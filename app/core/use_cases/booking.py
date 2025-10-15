from app.api.schemas import PropertyBookingsCheckSchema
from app.core.repositories import PropertyBookingsRepo
from app.core.entities import PropertyBookingsCheckEntity

class PropertyBookingsUseCase:
    def __init__(
        self,
        property_bookings_repo: PropertyBookingsRepo
    ):
        self.property_bookings_repo = property_bookings_repo
    
    async def check_property_bookings(self, property_bookings_data: PropertyBookingsCheckSchema)->bool:
        property_bookings_data_entity = PropertyBookingsCheckEntity(**property_bookings_data.model_dump())
        return await self.property_bookings_repo.check_property_bookings(property_bookings_data_entity)


