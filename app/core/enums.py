from enum import Enum

class KycVerificationStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PENDING = "pending"

class BookingStatusEnum(str, Enum):
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    PENDING = 'pending'

class PaymentModeEnum(str, Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'

class PaymentStatusEnum(str, Enum):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'