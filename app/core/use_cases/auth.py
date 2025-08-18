from app.core.entities.user import User
from app.core.repositories.traveller.user_repository import UserRepository
from app.core.repositories.traveller.email_repo import EmailRepo
from app.infrastructure.redis.redis_client import RedisClient
from app.api.schemas.Traveller.authentication import UserRegisterSchema
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
        

