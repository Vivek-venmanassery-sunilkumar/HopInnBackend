from dataclasses import dataclass
from datetime import timedelta

#jwtsettings class to pass in to the token_repository_impl in infrastructure/repositories

@dataclass
class JWTSettingsEntity:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta
    REFRESH_TOKEN_EXPIRE_DAYS: timedelta
