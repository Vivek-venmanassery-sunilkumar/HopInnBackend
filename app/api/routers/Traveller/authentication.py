from app.api.schemas import OtpDataSchema, EmailSchema, LoginSchema, UserRegisterSchema, TokenRequestSchema
from app.api.dependencies import UserRepoDep, EmailRepoDep, RedisRepoDep, TokenRepoDep
from fastapi import APIRouter, HTTPException, status, Response, Request
from app.core.use_cases import SignUpUseCases, LoginUseCases, GoogleLoginUseCase, TokenUseCases
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup/initiate", status_code=status.HTTP_202_ACCEPTED)
async def initiate_signup(
    user_data: UserRegisterSchema,
    user_repo: UserRepoDep,
    redis_client: RedisRepoDep,
    email_repo: EmailRepoDep
):

    auth_uc = SignUpUseCases(user_repo, redis_client, email_repo)
    try:
        otp, email = await auth_uc.initiate_signup(user_data.model_dump())
        logger.info(otp)
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
    auth_uc = SignUpUseCases(user_repo, redis_client, email_repo)
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
    auth_uc = SignUpUseCases(user_repo, redis_client, email_repo)
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


@router.post('/login', status_code= status.HTTP_200_OK)
async def login(
    login_data: LoginSchema,
    user_repo: UserRepoDep,
    token_repo: TokenRepoDep,
    response: Response
):
    login_uc = LoginUseCases(user_repo, token_repo)

    try:
        user_response, tokens = await login_uc.execute(login_data.email, login_data.password)
        
        response.set_cookie(
            key="access_token",
            value = tokens["access_token"],
            httponly= True,
            secure = False,
            max_age = 15*60,
            samesite="lax",
            path='/'
        )
        response.set_cookie(
            key="refresh_token",
            value = tokens["refresh_token"],
            httponly=True,
            secure = False,
            max_age = 30*24*60*60,
            samesite='lax',
            path='/'
        )

        return {
            "user": user_response,
            "message": "Login successful"
        }
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = {
                'status':'error',
                'message': str(e)
            }
        )

@router.post('/google', status_code=status.HTTP_200_OK)
async def google_login(
    data: TokenRequestSchema,
    user_repo: UserRepoDep,
    token_repo: TokenRepoDep,
    response: Response
):
    google_uc = GoogleLoginUseCase(user_repo=user_repo, token_repo=token_repo)

    try:
        user_response, tokens = await google_uc.execute(data.token)

        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
            secure = False,
            max_age = 30*24*60*60,
            samesite='lax',
            path='/'
        )
        
        response.set_cookie(
            key="refresh_token",
            value = tokens["refresh_token"],
            httponly=True,
            secure = False,
            max_age = 30*24*60*60,
            samesite='lax',
            path='/'
        )

        return {
            "user": user_response,
            "message": "google login successfull"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'status': 'error',
                'message': str(e)
            }
        )
    except Exception as e:
        logger.info(f"Unexpected error in Google login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'status': 'error',
                'message': 'Internal server error during Google authentication'
            }
        )


@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh_token(
    request: Request,
    response: Response,
    token_repo: TokenRepoDep, 
    redis_repo: RedisRepoDep,
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "Refresh token not found"}
        )
    
    token_uc = TokenUseCases(token_repo, redis_repo)

    try:
        access_token, refresh_token = await token_uc.rotate_tokens(refresh_token)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            max_age=15*60,
            samesite='lax',
            path='/'
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            max_age=30*24*60*60,
            samesite='lax',
            path='/'
        )
        return {"status": "success", "message": "Token refreshed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": str(e)}
        )
    except Exception as e:
        logger.info(f"Unexpected error in refresh token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": "Internal server error during token refresh"}
        )
    