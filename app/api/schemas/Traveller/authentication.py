from pydantic import BaseModel
from app.core.validations.types import StrictEmail
from app.core.validations.decorators import password_validator, otp_validator
from typing import Optional

class UserRegisterSchema(BaseModel):
    fullName: str
    phoneNumber: str
    email: StrictEmail
    password: str
    
    _validate_password = password_validator("password")

class OtpDataSchema(BaseModel):
    email: StrictEmail
    otp: str

    _validate_otp = otp_validator("otp")

class EmailSchema(BaseModel):
    email: StrictEmail

class LoginSchema(BaseModel):
    email: StrictEmail
    password: str

    _validate_password = password_validator("password")

class SafeUserResponse(BaseModel):
    id: str
    isAdmin: bool
    isGuide: bool
    isHost: bool 
    isTraveller: bool 
    isActive: bool