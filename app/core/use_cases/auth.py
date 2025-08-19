from app.core.entities.user import User
from app.core.repositories.traveller.user_repository import UserRepository
from app.core.repositories.token.token_repository import TokenRepository
from app.core.repositories.traveller.email_repo import EmailRepo
from app.infrastructure.redis.redis_client import RedisClient
from app.api.schemas.Traveller.authentication import UserRegisterSchema, SafeUserResponse
from typing import Dict, Any
import random
import string

class SignUpUseCases:
    def __init__(
            self, 
            user_repo: UserRepository, 
            redis_client: RedisClient,
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
    
    async def create_user(self, user_data: UserRegisterSchema)->User:
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
        user_response = SafeUserResponse(
            id=user.id,
            isAdmin=user.is_admin,
            isGuide=user.is_guide,
            isHost = user.is_host,
            isTraveller=user.is_traveller,
            isActive = user.is_active,
        )
        tokens = self._generate_tokens(user.id)
        return user_response, tokens 
    async def _validate_user(self, email: str)->User:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        return user
    
    async def _validate_password(self, password: str, hashed_password: str)->bool:
        validated = await self.user_repo.verify_password(password, hashed_password)
        if not validated:
            raise ValueError("You entered the wrong password")
    

    def _generate_tokens(self,user_id: str)->dict:
        access_token = self.token_repo.generate_access_token(user_id)
        refresh_token = self.token_repo.generate_refresh_token(user_id)
        return {'access_token': access_token, 'refresh_token': refresh_token}

        
