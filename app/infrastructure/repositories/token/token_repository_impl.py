from app.core.repositories.token.token_repository import TokenRepository
from app.core.entities.jwt_settings import JWTSettings
from jose import jwt, JWTError
from datetime import datetime
from app.core.redis.redis_repo import RedisRepoInterface
from typing import Optional


class TokenRepositoryImpl(TokenRepository):
    def __init__(self, jwt_settings: JWTSettings, redis_client = RedisRepoInterface):
        self.jwt_settings = jwt_settings
        self.redis_client = redis_client

    def generate_access_token(self, user_id: str)->str:
        access_token = jwt.encode(
            claims = {
                'user_id': user_id,
                'type':"access",
                "exp": datetime.utcnow() + self.jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
            },
            key = self.jwt_settings.SECRET_KEY,
            algorithm = self.jwt_settings.ALGORITHM
        )
        return access_token

    def generate_refresh_token(self,user_id: str)->str:
        refresh_token = jwt.encode(
            claims={
                'user_id': user_id,
                'type': "refresh",
                "exp": datetime.utcnow() + self.jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS
            },
            key = self.jwt_settings.SECRET_KEY,
            algorithm=self.jwt_settings.ALGORITHM
        ) 
        return refresh_token
    
    def verify_access_token(self, token: str)->Optional[dict]:
        try:
            payload = jwt.decode(token, self.jwt_settings.SECRET_KEY, algorithms=self.jwt_settings.ALGORITHM)

            #check expiration
            exp = payload.get('exp')
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                return None
            
            return payload
        except JWTError:
            return None
        
    def decode_token(self, token: str)->Optional[dict]:
        try:
            payload = jwt.decode(
                token,
                self.jwt_settings.SECRET_KEY,
                algorithms=self.jwt_settings.ALGORITHM
            )
            return payload
        except JWTError:
            return None

