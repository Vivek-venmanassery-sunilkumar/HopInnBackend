from app.core.entities import UserEntity
from app.api.schemas import UserRolesSchema,UserRegisterSchema, SafeUserResponseSchema
from app.core.repositories import UserRepository, TokenRepository, EmailRepo
from app.core.redis.redis_repo import RedisRepoInterface
from typing import Dict, Any, Tuple
import random
import string
import logging

logger = logging.getLogger(__name__)

class SignUpUseCases:
    def __init__(
            self, 
            user_repo: UserRepository, 
            redis_client: RedisRepoInterface,
            email_repo: EmailRepo
            ):
        self.user_repo = user_repo
        self.redis_client = redis_client
        self.email_repo = email_repo
    
    def generate_otp(self)->str:
        return ''.join(random.choices(population=string.digits, k=6))
    
    async def initiate_signup(self, user_data: Dict[str, Any]) -> tuple:
        email = user_data["email"]
        if await self.user_repo.get_user_by_email(email=email):
            raise ValueError("User already exists")
        
        otp = self.generate_otp()
        await self.redis_client.store_signup_data(
            email=email,
            otp = otp,
            user_data = user_data
        )

        return otp, email

    async def verify_otp(self, email: str, otp: str)->dict:
        data = await self.redis_client.get_signup_data(email)
        if not data:
            raise ValueError("You took too long hence expired")    
        if data['attempts'] == 3:
            raise ValueError("Max attempt reached! Validate with a new otp after countdown.")
        if data["otp"] != otp:
            attempts = data['attempts'] + 1
            if attempts == 3:
                raise ValueError("Invalid OTP.Max attempt reached! Validate with a new otp after countdown.")
            await self.redis_client.update_signup_data(email = email, attempts = attempts)
            raise ValueError("Invalid OTP")

        await self.redis_client.delete_signup_data(email=email) 
        return data["user_data"]
    
    async def create_user(self, user_data: UserRegisterSchema)->UserEntity:
        return await self.user_repo.create_user(user_data)
    
    def send_email(self, email: str, otp: str)->None:
        self.email_repo.send(email, otp)
    
    async def retry_otp(self, email: str)->str:
        data = await self.redis_client.get_signup_data(email)
        if not data:
            raise ValueError("You took too long hence expired")
      #keeping the ttl same, increase the retry_attempts as necessary to complete the requirement for the retry otp endpoint.        
        new_otp = self.generate_otp()
        await self.redis_client.update_signup_data(
            email=email,
            otp= new_otp,
            otp_retry_attempts = data['otp_retry_attempts'] + 1,
            attempts = 0
        )
        return new_otp
        

class LoginUseCases:
    def __init__(
            self,
            user_repo: UserRepository,
            token_repo: TokenRepository,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
    
    async def execute(self, email: str, password: str)->tuple:
        user = await self._validate_user(email)
        await self._validate_password(password, user.password_hash)
        user_response = SafeUserResponseSchema(
            id=user.id,
            isAdmin=user.is_admin,
            isGuide=user.is_guide,
            isHost = user.is_host,
            isTraveller=user.is_traveller,
            isActive = user.is_active,
        )
        tokens = self._generate_tokens(user.id)
        return user_response, tokens 
    async def _validate_user(self, email: str)->UserEntity:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        logger.info(f'user status: {user.is_active}')
        if user.password_hash is None and user.google_id:
            raise ValueError("This account uses Google authentication. Please sign in with Google.")
        if not user.is_active:
            raise ValueError("This account is banned by the admin")
        return user
    
    async def _validate_password(self, password: str, hashed_password: str)->bool:
        validated = await self.user_repo.verify_password(password, hashed_password)
        if not validated:
            raise ValueError("You entered the wrong password")
    

    def _generate_tokens(self,user_id: str)->dict:
        access_token = self.token_repo.generate_access_token(user_id)
        refresh_token = self.token_repo.generate_refresh_token(user_id)
        return {'access_token': access_token, 'refresh_token': refresh_token}

        

class RolesUseCase:
    def __init__(
            self,
            user_repo: UserRepository
    ):
        self.user_repo = user_repo

    def get_roles(self, user_id:str)->UserRolesSchema:
        return self.user_repo.get_user_roles(user_id)


class GoogleLoginUseCase:
    def __init__(
            self, 
            user_repo: UserRepository,
            token_repo: TokenRepository
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def execute(self, google_token: str)->Tuple[SafeUserResponseSchema, dict]:
        #Verify google token and get user info
        user_info = await self._verify_google_token(google_token)
        email = user_info['email']
        google_id = user_info['sub']
        picture = user_info.get('picture', '')

        user = await self.user_repo.get_user_by_email(email)
        if user:
            if not user.is_active:
                raise ValueError("The user is blocked by the admin")
            if not user.google_id or user.google_id != google_id:
                success = await self.user_repo.update_google_user_info(email, google_id, picture)

                if not success:
                    raise ValueError("Failed to update user Google information")

                user = await self.user_repo.get_user_by_email(email)
        else:
            success = await self.user_repo.create_google_user(
                email=email,
                name=user_info.get('name',''),
                google_id = google_id,
                picture=picture
            )

            if not success:
                raise ValueError("Failed to create new user")

            user = await self.user_repo.get_user_by_email(email)
        
        user_response =self._generate_user_response(user)
        tokens = self._generate_tokens(user.id)

        return user_response, tokens

    async def _verify_google_token(self, google_token: str)->dict:
        idinfo = await self.user_repo.verify_google_token(google_token)
        if not idinfo.get('email') or not idinfo.get('sub'):
            raise ValueError("Invalid Google token: missing required user information")

        if not idinfo.get('email_verified', False):
            raise ValueError("Google email not verified")
        
        return idinfo

    def _generate_user_response(self, user: UserEntity)->SafeUserResponseSchema:
        return SafeUserResponseSchema(
            id=user.id,
            isAdmin=user.is_admin,
            isGuide=user.is_guide,
            isHost = user.is_host,
            isTraveller=user.is_traveller,
            isActive = user.is_active
        )
    
    def _generate_tokens(self, user_id: str)->dict:
        access_token = self.token_repo.generate_access_token(user_id)
        refresh_token = self.token_repo.generate_refresh_token(user_id)
        return {'access_token': access_token, 'refresh_token': refresh_token}



    

        