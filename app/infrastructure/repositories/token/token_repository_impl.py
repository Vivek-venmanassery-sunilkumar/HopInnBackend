from app.core.repositories.token.token_repository import TokenRepository
from app.config.jwt_settings import jwt_settings
from jose import jwt
from datetime import datetime, timedelta


class TokenRepositoryImpl(TokenRepository):
    def generate_access_token(self, user_id: str)->str:
        access_token = jwt.encode(
            claims = {
                'sub': user_id,
                'type':"access",
                "exp": datetime.utcnow() + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            },
            key = jwt_settings.SECRET_KEY,
            algorithm = jwt_settings.ALGORITHM
        )

        return access_token

    def generate_refresh_token(self,user_id: str)->str:
        refresh_token = jwt.encode(
            claims={
                'sub': user_id,
                'type': "refresh",
                "exp": datetime.utcnow() + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
            },
            key = jwt_settings.SECRET_KEY,
            algorithm=jwt_settings.ALGORITHM
        ) 

        return refresh_token
    

    
