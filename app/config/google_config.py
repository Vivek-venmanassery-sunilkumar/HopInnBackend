from pydantic_settings import BaseSettings, SettingsConfigDict

class GoogleSettings(BaseSettings):
    CLIENT_ID: str

    model_config = SettingsConfigDict(env_prefix='GOOGLE_', env_file='.env', extra='ignore')

google_settings = GoogleSettings()