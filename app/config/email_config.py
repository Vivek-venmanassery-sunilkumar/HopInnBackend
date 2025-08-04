from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailSettings(BaseSettings):
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    FROM_EMAIL: str

    model_config = SettingsConfigDict(env_prefix="SMTP_", env_file=".env", extra="ignore")

email_settings = EmailSettings()