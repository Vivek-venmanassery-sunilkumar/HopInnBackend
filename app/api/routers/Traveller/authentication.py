from app.api.schemas.Traveller.authentication import UserRegister
from app.api.dependencies import UserRepoDep, EmailRepoDep, RedisRepoDep
from fastapi import APIRouter, HTTPException, status
from app.core.use_cases.auth import AuthUseCases
from app.config.redis import redis_settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup/initiate", status_code=status.HTTP_202_ACCEPTED)
async def initiate_signup(
    user_data: UserRegister,
    user_repo: UserRepoDep,
    redis_client: RedisRepoDep,
    email_repo: EmailRepoDep
):

    auth_uc = AuthUseCases(user_repo, redis_client, email_repo)
    try:
        otp = await auth_uc.initiate_signup(user_data.model_dump())
        return {
            "status": "success",
            "message": "OTP sent to email",
            "data": {
                "email": user_data.email,
                "otp_expiry_seconds": redis_settings.OTP_EXPIRE_SECONDS
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "status": "error",
                "message": str(e),
                "code": "USER_ALREADY_EXISTS" if "already exists" in str(e) else "VALIDATION_ERROR"
            }
        )

