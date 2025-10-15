from enum import Enum

class KycVerificationStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PENDING = "pending"

class BookingStatusEnum(str, Enum):
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

class PaymentModeEnum(str, Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'