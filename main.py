# Standard library imports
import os
from dotenv import load_dotenv

# FastAPI imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Application imports
from app.api.middlewares.jwt_middleware import JWTMiddleware
from app.api.dependencies import get_token_repository, get_redis_client
from app.infrastructure.config.jwt_settings_adaptor import get_core_jwt_settings
from app.infrastructure.config.redis_settings_adaptor import get_core_redis_settings
from app.core.logging_setup import setup_logging

# Router imports - organized by functionality
from app.api.routers import (
    # Authentication & Authorization
    auth_router,
    role_router,
    
    # User Management
    profile_router,
    kyc_router,
    
    # Onboarding
    onboard_router,
    guide_profile_router,
    host_profile_router,
    
    # Core Features
    property_router,
    home_page_filter_router,
    booking_properties_router,
    
    # External Services
    cloudinary_router,
    
    # Administration
    admin_router,
)

load_dotenv()
setup_logging()

app = FastAPI()


allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(',')

#done to obtain the dependencies for the dependencies that the JWT middleware require
jwt_settings = get_core_jwt_settings()
redis_client = get_core_redis_settings()

'''Following are the dependencies for the JWT middleware, this is explicitly done since fastapi dependency injection
doesnt work with annotated dependencies for middlewares
'''
redis_repo = get_redis_client(redis_settings=redis_client)
token_repo = get_token_repository(jwt_settings=jwt_settings, redis_client=redis_client)

#Add JWT middleware with exempt paths
app.add_middleware(
    JWTMiddleware,
    token_repo = token_repo,
    redis_repo= redis_repo,
    exempt_paths=['/auth','/docs', '/openapi.json']
)


#Add CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins = allowed_origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
    expose_headers=["*"]
)


# Include routers - organized by functionality
# Authentication & Authorization
app.include_router(auth_router)
app.include_router(role_router)

# User Management
app.include_router(profile_router)
app.include_router(kyc_router)

# Onboarding
app.include_router(onboard_router)
app.include_router(guide_profile_router)
app.include_router(host_profile_router)

# Core Features
app.include_router(property_router)
app.include_router(home_page_filter_router)
app.include_router(booking_properties_router)

# External Services
app.include_router(cloudinary_router)

# Administration
app.include_router(admin_router)