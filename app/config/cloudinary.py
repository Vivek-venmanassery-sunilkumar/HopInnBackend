from pydantic_settings import BaseSettings, SettingsConfigDict
import cloudinary

class CloudinarySettings(BaseSettings):
    NAME: str
    API_KEY: str
    API_SECRET: str


    model_config=SettingsConfigDict(env_prefix='CLOUD_', env_file='.env', extra='ignore')

cloud_settings = CloudinarySettings()


cloud_config = cloudinary.config(
    cloud_name = cloud_settings.NAME,
    api_key = cloud_settings.API_KEY,
    api_secret = cloud_settings.API_SECRET,
    secure = True
)


