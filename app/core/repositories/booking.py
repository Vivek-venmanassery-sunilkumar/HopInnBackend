from abc import ABC, abstractmethod
from app.core.entities import PropertyBookingsCheckEntity


class PropertyBookingsRepo(ABC):
    @abstractmethod
    async def check_property_bookings(self, property_bookings_data: PropertyBookingsCheckEntity)->bool:
        pass

    @abstractmethod
    async def calculate_property_booking_amount(self, property_bookings_data: PropertyBookingsCheckEntity)->float:
        pass