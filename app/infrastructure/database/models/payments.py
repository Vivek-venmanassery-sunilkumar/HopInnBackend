from app.infrastructure.database.session import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.core.enums import PaymentStatusEnum

class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    traveller_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    host_id = Column(Integer, ForeignKey('host.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_mode = Column(String(255), nullable=False)
    payment_status = Column(String(255), default = PaymentStatusEnum.PENDING)
    transaction_id = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)