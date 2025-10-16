from fastapi import APIRouter, status, Depends, HTTPException
from app.core.route_protection_validations.route_protection_dependencies import verify_traveller
from app.api.schemas import PropertyBookingsCheckSchema
from app.api.dependencies import BookingRepoDep
from app.core.use_cases import PropertyBookingsUseCase


router = APIRouter(prefix='/booking-properties', tags=['booking-properties'])


@router.post('/check', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def property_book_check_and_calculate_amount(
    property_book_check_data: PropertyBookingsCheckSchema,
    booking_repo: BookingRepoDep
):
    property_bookings_uc = PropertyBookingsUseCase(property_bookings_repo = booking_repo)
    property_bookings_check = await property_bookings_uc.check_property_bookings(property_book_check_data)
    if property_bookings_check:
        property_bookings_amount = await property_bookings_uc.calculate_property_booking_amount(property_book_check_data)
        return {
            "success": True,
            "message": "User can book the property",
            "propertyId": property_book_check_data.propertyId,
            "amount": property_bookings_amount,
            "numAdults": property_book_check_data.numAdults,
            "numChildren": property_book_check_data.numChildren,
            "numInfants": property_book_check_data.numInfants,
            "totalGuests": property_book_check_data.totalGuests,
            'checkInDate': property_book_check_data.checkInDate,
            'checkOutDate': property_book_check_data.checkOutDate
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="These dates are not available for booking"
        )

@router.post('/add-guests', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_traveller)])
async def add_guests(
    booking_repo: BookingRepoDep
):
    pass