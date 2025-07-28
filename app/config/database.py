
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str
    DB_ECHO_LOG: bool = False

    model_config = SettingsConfigDict(env_file = ".env") 

db_settings = DatabaseSettings()