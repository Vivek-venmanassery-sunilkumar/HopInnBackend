from dataclasses import dataclass



@dataclass
class RedisSettingsEntity:
    HOST: str
    PORT: int
    DB: int
    PASSWORD: str | None
    OTP_EXPIRE_SECONDS: int
    MAX_OTP_ATTEMPTS: int
    MAX_OTP_RETRY_ATTEMPTS: int