from .Traveller.authentication import UserRegisterSchema, OtpDataSchema, EmailSchema, LoginSchema, SafeUserResponseSchema
from .Traveller.profile import TravellerProfileSchema
from .Traveller.kyc import KycSchema, KycResponseSchema
from .roles.roles import UserRolesSchema
from .cloudinary_schema import CloudDataSchema