
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    URL: str
    ECHO_LOG: bool = False

    model_config = SettingsConfigDict(env_prefix="DB_", env_file = ".env", extra="ignore") 

db_settings = DatabaseSettings()