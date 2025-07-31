from pydantic_settings import BaseSettings, SettingsConfigDict

class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    OTP_EXPIRE_SECONDS: int = 300
    MAX_OTP_ATTEMPTS: int = 3

    model_config = SettingsConfigDict(env_file = ".env")

redis_settings = RedisSettings()