from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_db
from app.core.repositories import UserRepository, EmailRepo, TokenRepository,TravellerProfileInterface, UserRolesPermissionsInterface, KycRepo, OnboardRepo, GuideProfileInterface, HostProfileInterface
from app.infrastructure.repositories import SQLAlchemyUserRepository, CeleryEmailRepo, TokenRepositoryImpl
from app.infrastructure.redis.redis_client import RedisClient
from app.infrastructure.config.jwt_settings_adaptor import get_core_jwt_settings
from app.infrastructure.config.redis_settings_adaptor import get_core_redis_settings
from app.infrastructure.config.google_settings_adaptor import get_core_google_settings
from app.core.entities import JWTSettingsEntity, RedisSettingsEntity, GoogleSettingsEntity
from app.core.redis.redis_repo import RedisRepoInterface
from app.infrastructure.repositories import TravellerProfileImpl, UserRolesPermissionsImpl, KycRepoImpl, OnboardRepoImpl, GuideProfileImpl, HostProfileImpl


'''get_user_roles_permissions is a dependecy injection function that is to be used
    internally for validation decorators for route protection inside app/core/validations/decorators.py
'''

DbDep = Annotated[AsyncSession, Depends(get_db)]
async def get_user_roles_permissions(
        db: DbDep
)->UserRolesPermissionsInterface:
    return UserRolesPermissionsImpl(db)

async def get_user_repository(
        db: DbDep,
        google_client: Annotated[GoogleSettingsEntity, Depends(get_core_google_settings)]
)-> UserRepository:
    return SQLAlchemyUserRepository(db, google_client)

async def get_guide_profile_repository(
        db:DbDep
)->GuideProfileInterface:
    return GuideProfileImpl(db)

async def get_host_profile_repository(
        db:DbDep
)->HostProfileInterface:
    return HostProfileImpl(db)

async def get_onboard_repository(
        db:DbDep,
)->OnboardRepo:
    return OnboardRepoImpl(db)

def get_email_repository()->EmailRepo:
    return CeleryEmailRepo()

def get_redis_client(
        redis_settings: Annotated[RedisSettingsEntity, Depends(get_core_redis_settings)]
)->RedisClient:
    return RedisClient(redis_settings)

async def get_traveller_profile_repo(
        db: DbDep
)->TravellerProfileInterface:
    return TravellerProfileImpl(db)

async def get_kyc_repo(
        db: DbDep
)->KycRepo:
    return KycRepoImpl(db)

HostProfileDep = Annotated[HostProfileInterface, Depends(get_host_profile_repository)]
GuideProfileDep = Annotated[GuideProfileInterface, Depends(get_guide_profile_repository)]
UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
EmailRepoDep = Annotated[EmailRepo, Depends(get_email_repository)]
RedisRepoDep = Annotated[RedisRepoInterface, Depends(get_redis_client)]
TravellerProfileDep = Annotated[TravellerProfileInterface, Depends(get_traveller_profile_repo)]
KycRepoDep = Annotated[KycRepo, Depends(get_kyc_repo)]
OnboardRepoDep = Annotated[OnboardRepo, Depends(get_onboard_repository)]

def get_token_repository(
        jwt_settings: Annotated[JWTSettingsEntity, Depends(get_core_jwt_settings)],
        redis_client: RedisRepoDep
)->TokenRepository:
    return TokenRepositoryImpl(jwt_settings, redis_client)
TokenRepoDep = Annotated[TokenRepository, Depends(get_token_repository)]