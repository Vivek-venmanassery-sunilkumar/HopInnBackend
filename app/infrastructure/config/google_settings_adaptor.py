from app.core.entities import GoogleSettingsEntity
from app.config.google_config import google_settings

def get_core_google_settings()->GoogleSettingsEntity:
    return GoogleSettingsEntity(
        CLIENT_ID=google_settings.CLIENT_ID
    )