from pydantic import EmailStr
from app.core.validations.regex_patterns.validation_patterns import EMAIL_PATTERN


class StrictEmail(EmailStr):
    @classmethod
    def __get_validators__(cls):
        yield from EmailStr.__get_validators__()
        yield cls.validate_pattern

    @classmethod
    def validate_pattern(cls, value):
        if not EMAIL_PATTERN.match(value):
            raise ValueError("Invalid email format")
        return value