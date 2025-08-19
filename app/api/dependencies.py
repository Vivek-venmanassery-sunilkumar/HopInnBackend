from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_db
from app.core.repositories import UserRepository, EmailRepo, TokenRepository
from app.infrastructure.repositories import SQLAlchemyUserRepository, CeleryEmailRepo, TokenRepositoryImpl
from app.infrastructure.redis.redis_client import RedisClient



async def get_user_repository(
        db: Annotated[AsyncSession, Depends(get_db)]
)-> UserRepository:
    return SQLAlchemyUserRepository(db)

def get_email_repository()->EmailRepo:
    return CeleryEmailRepo()

def get_redis_client()->RedisClient:
    return RedisClient()

def get_token_repository()->TokenRepository:
    return TokenRepositoryImpl()

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
EmailRepoDep = Annotated[EmailRepo, Depends(get_email_repository)]
RedisRepoDep = Annotated[RedisClient, Depends(get_redis_client)]
TokenRepoDep = Annotated[TokenRepository, Depends(get_token_repository)]