from pydantic import field_validator
from app.core.validations.regex_patterns.validation_patterns import PASSWORD_PATTERN


#field validators in schema

def password_validator(field_name="password"):
    @field_validator(field_name)
    def __validate_password(cls, v):
        if not PASSWORD_PATTERN.match(v):
            raise ValueError("Password does not meet complexity requirements")
        return v
    return __validate_password

def otp_validator(field_name="otp"):
    @field_validator(field_name)
    def __validate_otp(cls, v):
        if len(v) != 6:
            raise ValueError("Otp should be 6 digits")
        return v
    return __validate_otp

