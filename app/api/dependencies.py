from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_db
from app.core.repositories import UserRepository, EmailRepo, TokenRepository,TravellerProfileInterface, UserRolesPermissionsInterface
from app.infrastructure.repositories import SQLAlchemyUserRepository, CeleryEmailRepo, TokenRepositoryImpl
from app.infrastructure.redis.redis_client import RedisClient
from app.infrastructure.config.jwt_settings_adaptor import get_core_jwt_settings
from app.infrastructure.config.redis_settings_adaptor import get_core_redis_settings
from app.core.entities.jwt_settings import JWTSettings
from app.core.entities.redis_settings import RedisSettings
from app.core.redis.redis_repo import RedisRepoInterface
from app.infrastructure.repositories import TravellerProfileImpl, UserRolesPermissionsImpl


'''get_user_roles_permissions is a dependecy injection function that is to be used
    internally for validation decorators for route protection inside app/core/validations/decorators.py
'''
async def get_user_roles_permissions(
        db: Annotated[AsyncSession, Depends(get_db)]
)->UserRolesPermissionsInterface:
    return UserRolesPermissionsImpl(db)

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

async def get_traveller_profile_repo(
        db: Annotated[AsyncSession,Depends(get_db)]
)->TravellerProfileInterface:
    return TravellerProfileImpl(db)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
EmailRepoDep = Annotated[EmailRepo, Depends(get_email_repository)]
RedisRepoDep = Annotated[RedisRepoInterface, Depends(get_redis_client)]
TravellerProfileDep = Annotated[TravellerProfileInterface, Depends(get_traveller_profile_repo)]

def get_token_repository(
        jwt_settings: Annotated[JWTSettings, Depends(get_core_jwt_settings)],
        redis_client: RedisRepoDep
)->TokenRepository:
    return TokenRepositoryImpl(jwt_settings, redis_client)
TokenRepoDep = Annotated[TokenRepository, Depends(get_token_repository)]