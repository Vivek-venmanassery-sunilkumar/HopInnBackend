from app.core.repositories.booking import PropertyBookingsRepo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.core.entities import PropertyBookingsCheckEntity
from app.core.enums import BookingStatusEnum
from app.infrastructure.database.models.booking import PropertyBookings
from app.infrastructure.database.models.onboard import Property
import logging

logger = logging.getLogger(__name__)


class PropertyBookingsRepoImpl(PropertyBookingsRepo):
    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session
    
    async def check_property_bookings(self, property_bookings_data: PropertyBookingsCheckEntity) -> bool:
        """
        Check if a property is available for booking based on:
        1. Date range availability (no overlapping CONFIRMED bookings)
        2. Guest capacity (total_guests <= max_guests)
        
        Note: Only considers CONFIRMED bookings for overlap checking.
        COMPLETED and CANCELLED bookings are ignored.
        
        Returns True if available, False otherwise
        """
        try:
            # First, check if the property exists and get its max_guests
            property_query = select(Property.max_guests).where(Property.id == property_bookings_data.property_id)
            property_result = await self.session.execute(property_query)
            property_data = property_result.scalar_one_or_none()
            
            if not property_data:
                # Property doesn't exist
                return False
            
            max_guests = property_data
            
            # Check if total_guests exceeds property capacity
            if property_bookings_data.total_guests > max_guests:
                return False
            
            # Check for overlapping bookings
            # A booking overlaps if:
            # - New check-in is before existing check-out AND new check-out is after existing check-in
            # - Only consider CONFIRMED bookings (exclude COMPLETED and CANCELLED)
            overlapping_query = select(PropertyBookings.id).where(
                and_(
                    PropertyBookings.property_id == property_bookings_data.property_id,
                    PropertyBookings.booking_status == BookingStatusEnum.CONFIRMED.value,
                    PropertyBookings.check_in_date < property_bookings_data.check_out_date,
                    PropertyBookings.check_out_date > property_bookings_data.check_in_date
                )
            )
            
            overlapping_result = await self.session.execute(overlapping_query)
            overlapping_bookings = overlapping_result.scalars().all()
            
            # If there are overlapping bookings, property is not available
            if overlapping_bookings:
                return False
            
            # If we reach here, property is available
            return True
            
        except Exception as e:
            # Log the error (you might want to use a proper logger)
            logger.error(f"Error checking property bookings: {e}")
            return False