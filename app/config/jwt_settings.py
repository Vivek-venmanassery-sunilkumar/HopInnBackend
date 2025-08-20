from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets

#main settings for the jwt from the enviornment file

class JWTSettings(BaseSettings):
    SECRET_KEY: str = secrets.token_hex(32)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  

    model_config = SettingsConfigDict(
        env_prefix='JWT_',
        env_file='.env',
        extra='ignore'
    )

jwt_settings = JWTSettings()