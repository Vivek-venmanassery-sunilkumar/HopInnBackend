from pydantic import BaseModel, EmailStr, field_validator
import re

class UserRegister(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr
    password: str


    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password too short")
        if not re.search(r"\d", v):
            raise ValueError("Password needs a number")
        return v
    
    @field_validator("phone_number")
    def validate_phone(cls, v):
        try:
            parsed = parse(v, None)
            return format_number(parsed, PhoneNumberFormat.E164)
        except NumberParseException:
            raise ValueError("Invalid phone number. Include country code (e.g., +1)")