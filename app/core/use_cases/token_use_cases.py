from app.core.repositories import TokenRepository
from app.core.redis.redis_repo import RedisRepoInterface
from typing import Optional

class TokenUseCases:
    def __init__(
            self,
            token_repo: TokenRepository,
            redis_repo: RedisRepoInterface
    ):
        self.token_repo = token_repo
        self.redis_repo = redis_repo

    async def verify_access_token(self, token:str)->Optional[dict]:
        if not token:
            return None

        if await self.redis_repo.is_token_blacklisted(token):
            return None
        
        return self.token_repo.verify_access_token(token)
    
    async def verify_refresh_token(self, token:str)->Optional[dict]:
        if not token:
            return None
        if await self.redis_repo.is_token_blacklisted(token):
            return None

        return self.token_repo.verify_refresh_token(token)
    
    async def extract_user_id(self, token: str)->Optional[str]:
        """Extract user_id from JWT token"""
        payload = self.token_repo.decode_token(token)
        if payload and 'user_id' in payload:
            return payload['user_id']
        return None
    
    def generate_access_token(self, user_id: str)->str:
        return self.token_repo.generate_access_token(user_id)
    
    def generate_refresh_token(self, user_id:str)->str:
        return self.token_repo.generate_refresh_token(user_id)
    
    async def blacklist_token(self, token:str, expiry:int)->None:
        await self.redis_repo.store_blacklisted_token(token, expiry)
    

    async def rotate_tokens(self, token: str)->Optional[tuple[str, str]]:
        token_data = await self.verify_refresh_token(token)
        if not token_data:
            raise ValueError("Invalid refresh token")
        user_id = token_data.get('user_id')
        if not user_id:
            raise ValueError("Invalid refresh token")
        access_token = self.generate_access_token(user_id)
        await self.blacklist_token(token, 30*24*60*60)
        refresh_token = self.generate_refresh_token(user_id)
        return access_token, refresh_token

