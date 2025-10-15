from fastapi import APIRouter, status, Depends, HTTPException
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller
from app.api.schemas import PropertyBookingsCheckSchema
from app.api.dependencies import BookingRepoDep
from app.core.use_cases import PropertyBookingsUseCase


router = APIRouter(prefix='/booking-properties', tags=['booking-properties'])


@router.post('/check', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def property_book_check(
    property_book_check_data: PropertyBookingsCheckSchema,
    booking_repo: BookingRepoDep
):
    property_bookings_uc = PropertyBookingsUseCase(booking_repo = booking_repo)
    property_bookings_check = await property_bookings_uc.check_property_bookings(property_book_check_data)
    if property_bookings_check:
        return {
            "success": True,
            "message": "User can book the property"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="These dates are not available for booking"
        )