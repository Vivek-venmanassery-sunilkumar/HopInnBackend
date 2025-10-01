from pydantic import BaseModel, field_validator
from app.core.validations.types import StrictEmail
from app.core.validations.decorators import password_validator, otp_validator

class UserRegisterSchema(BaseModel):
    firstName: str
    lastName: str
    phoneNumber: str
    email: StrictEmail
    password: str
    
    _validate_password = password_validator("password")
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        # Truncate password to 72 bytes to avoid bcrypt error
        password_bytes = v.encode('utf-8')
        original_length = len(password_bytes)
        
        if original_length > 72:
            # Truncate to 72 bytes, not 72 characters
            v = password_bytes[:72].decode('utf-8', errors='ignore')
            print(f"DEBUG: Registration password truncated from {original_length} bytes to {len(v.encode('utf-8'))} bytes")
        
        return v

class OtpDataSchema(BaseModel):
    email: StrictEmail
    otp: str

    _validate_otp = otp_validator("otp")

class EmailSchema(BaseModel):
    email: StrictEmail

class LoginSchema(BaseModel):
    email: StrictEmail
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        # Truncate password to 72 bytes to avoid bcrypt error
        password_bytes = v.encode('utf-8')
        original_length = len(password_bytes)
        
        if original_length > 72:
            # Truncate to 72 bytes, not 72 characters
            v = password_bytes[:72].decode('utf-8', errors='ignore')
            print(f"DEBUG: Login password truncated from {original_length} bytes to {len(v.encode('utf-8'))} bytes")
        
        return v

class SafeUserResponseSchema(BaseModel):
    id: str
    isAdmin: bool
    isGuide: bool
    isHost: bool 
    isTraveller: bool 
    isActive: bool

class TokenRequestSchema(BaseModel):
    token: str