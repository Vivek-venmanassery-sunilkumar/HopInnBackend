from app.api.schemas.Traveller.authentication import UserRegisterSchema, OtpDataSchema, EmailSchema
from app.api.dependencies import UserRepoDep, EmailRepoDep, RedisRepoDep
from fastapi import APIRouter, HTTPException, status
from app.core.use_cases.auth import AuthUseCases

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup/initiate", status_code=status.HTTP_202_ACCEPTED)
async def initiate_signup(
    user_data: UserRegisterSchema,
    user_repo: UserRepoDep,
    redis_client: RedisRepoDep,
    email_repo: EmailRepoDep
):

    auth_uc = AuthUseCases(user_repo, redis_client, email_repo)
    try:
        otp, email = await auth_uc.initiate_signup(user_data.model_dump())
        auth_uc.send_email(email=email, otp=otp)
        return {
            "status": "success",
            "message": "OTP sent to email",
            "data": {
                "email": email,
                "otp_expiry_seconds": 60
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


@router.post("/signup/otp-verify", status_code=status.HTTP_201_CREATED)
async def otp_verify(
    otp_data: OtpDataSchema,
    user_repo: UserRepoDep,
    redis_client: RedisRepoDep,
    email_repo: EmailRepoDep
):
    auth_uc = AuthUseCases(user_repo, redis_client, email_repo)
    try:
        data = await auth_uc.verify_otp(email=otp_data.email, otp = otp_data.otp)
        success = await auth_uc.create_user(UserRegisterSchema(**data))
        if success:
            return {
                "status": "success",
                "message": "User created successfully",
            }
        else:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = {
                    'status': 'error',
                    'message': 'User already exists or could not be created'
                }
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": str(e),
            }
        )

@router.post("/signup/otp-retry", status_code=status.HTTP_200_OK)
async def retry_otp_send(
        email_data: EmailSchema, 
        user_repo: UserRepoDep,
        redis_client: RedisRepoDep,
        email_repo: EmailRepoDep
        ):
    auth_uc = AuthUseCases(user_repo, redis_client, email_repo)
    try:
        new_otp = await auth_uc.retry_otp(email_data.email)
        auth_uc.send_email(email=email_data.email, otp = new_otp)
        return {
            "status": "success",
            "message": "OTP resent successfully",
            "data":{
                "email": email_data.email,
                "otp_expiry_seconds": 60
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = {
                'status': 'error',
                'message': str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = {
                "status": "error",
                "message": "Something went wrong, please try again later"
            }
        )

