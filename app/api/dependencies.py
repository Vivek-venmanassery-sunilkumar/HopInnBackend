from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_db
from app.core.repositories import UserRepository, EmailRepo, TokenRepository
from app.infrastructure.repositories import SQLAlchemyUserRepository, CeleryEmailRepo, TokenRepositoryImpl
from app.infrastructure.redis.redis_client import RedisClient
from app.infrastructure.config.jwt_settings_adaptor import get_core_jwt_settings
from app.infrastructure.config.redis_settings_adaptor import get_core_redis_settings
from app.core.entities.jwt_settings import JWTSettings
from app.core.entities.redis_settings import RedisSettings
from app.core.redis.redis_repo import RedisRepoInterface




async def get_user_repository(
        db: Annotated[AsyncSession, Depends(get_db)]
)-> UserRepository:
    return SQLAlchemyUserRepository(db)

def get_email_repository()->EmailRepo:
    return CeleryEmailRepo()

def get_redis_client(
        redis_settings: Annotated[RedisSettings, Depends(get_core_redis_settings)]
)->RedisClient:
    return RedisClient(redis_settings)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
EmailRepoDep = Annotated[EmailRepo, Depends(get_email_repository)]
RedisRepoDep = Annotated[RedisRepoInterface, Depends(get_redis_client)]

def get_token_repository(
        jwt_settings: Annotated[JWTSettings, Depends(get_core_jwt_settings)],
        redis_client: RedisRepoDep
)->TokenRepository:
    return TokenRepositoryImpl(jwt_settings, redis_client)
TokenRepoDep = Annotated[TokenRepository, Depends(get_token_repository)]