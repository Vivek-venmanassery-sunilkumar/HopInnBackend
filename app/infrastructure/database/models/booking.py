from app.infrastructure.database.session import Base
from sqlalchemy import Column, Integer, ForeignKey, Date, String, DateTime, func
from app.core.enums import BookingStatusEnum, PaymentModeEnum


class PropertyBookings(Base):
    __tablename__ = 'property_bookings'

    id=Column(Integer, primary_key=True, autoincrement=True)
    traveller_id=Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    property_id=Column(Integer, ForeignKey('property.id', ondelete='CASCADE'), nullable=False)
    num_children=Column(Integer, default=0)
    num_adults=Column(Integer, nullable=False)
    num_infants=Column(Integer, default=0)
    total_guests=Column(Integer, nullable=False)
    check_in_date=Column(Date, nullable=False)
    check_out_date=Column(Date, nullable=False)
    payment_mode=Column(String(255), nullable=False, default=PaymentModeEnum.ONLINE)
    payment_id=Column(String(255), nullable=True)
    booking_status=Column(String(255), nullable=False, default=BookingStatusEnum.CONFIRMED)
    created_at=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)