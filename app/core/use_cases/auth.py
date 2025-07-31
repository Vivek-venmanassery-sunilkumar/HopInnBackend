from app.core.entities.user import User
from app.core.repositories.traveller.user_repository import UserRepository
from app.infrastructure.redis.redis_client import RedisClient
from typing import Dict, Any
import random
import string



class AuthUseCases:
    def __init__(self, user_repo: UserRepository, redis_client: RedisClient):
        self.user_repo = user_repo
        self.redis_client = redis_client
    
    async def initiate_signup(self, user_data: Dict[str, Any]) -> str:
        if await self.user_repo.get_user_by_email(user_data["email"]):
            raise ValueError("User already exists")
        
        otp = ''.join(random.choices(population=string.digits, k= 6))
        await self.redis_client.store_signup_data(
            email=user_data["email"],
            otp = otp,
            user_data = user_data
        )

        print(f"otp for {user_data['email']}: {otp}")
        return otp
    
    async def verify_otp_and_create_user(self, email: str, otp: str)-> User:
        user_data = await self.redis_client.verify_otp_and_retrieve_data(email, otp)
        if not user_data:
            raise ValueError("Invalid OTP or expired")
        return await self.user_repo.create_user(User(**user_data))