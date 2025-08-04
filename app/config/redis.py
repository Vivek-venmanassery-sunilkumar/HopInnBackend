from pydantic_settings import BaseSettings, SettingsConfigDict

class RedisSettings(BaseSettings):
    HOST: str
    PORT: int
    DB: int = 0
    PASSWORD: str | None = None
    OTP_EXPIRE_SECONDS: int = 300
    MAX_OTP_ATTEMPTS: int = 3

    model_config = SettingsConfigDict(env_prefix = "REDIS_", env_file = ".env", extra= "ignore")

redis_settings = RedisSettings()