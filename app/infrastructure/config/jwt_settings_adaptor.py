from datetime import timedelta
from app.core.entities.jwt_settings import JWTSettings
from app.config.jwt_settings import jwt_settings as infra_jwt_settings


#function to return the values from the jwt_settings config for the use of dependency injection to be used in the TokenRepoImpl in infra/repo

def get_core_jwt_settings()->JWTSettings:
    return JWTSettings(
        SECRET_KEY = infra_jwt_settings.SECRET_KEY,
        ALGORITHM=infra_jwt_settings.ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES=timedelta(minutes=infra_jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        REFRESH_TOKEN_EXPIRE_DAYS=timedelta(days=infra_jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )