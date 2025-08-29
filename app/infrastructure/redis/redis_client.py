import json
from redis import asyncio as aioredis
from app.core.entities import RedisSettingsEntity
from app.core.redis.redis_repo import RedisRepoInterface
import logging
logger = logging.getLogger(__name__)

class RedisClient(RedisRepoInterface):
    def __init__(self, redis_settings: RedisSettingsEntity):
        self.redis_settings = redis_settings
        self.client = aioredis.Redis(
            host = self.redis_settings.HOST,
            port = self.redis_settings.PORT,
            db = self.redis_settings.DB,
            password = self.redis_settings.PASSWORD or None,
            decode_responses= True,
            socket_connect_timeout = 5,
            )
    
    async def store_signup_data(self, email: str, otp: str, user_data: dict) ->None:
        key = f"signup:{email}"
        data = {
            "otp": otp,
            "user_data": user_data,
            "attempts": 0,
            "otp_retry_attempts": 0
        }
        success = await self.client.setex(
            name=key,
            time=self.redis_settings.OTP_EXPIRE_SECONDS,
            value = json.dumps(data)
        )
        logger.info(f"is the data saved: ", success)

    async def get_signup_data(self, email: str)->dict | None:
        key = f"signup:{email}"
        value = await self.client.get(key)
        if value is None:
            logger.info("signup_data found for: %s",email)
            return None

        if isinstance(value, bytes):
            value_str = value.decode("utf-8")
        else:
            value_str = value

        logger.info(f"Signup data for {email}: {value_str}")
        
        return json.loads(value) if value else None
    
    async def delete_signup_data(self, email: str)-> None:
        key = f"signup:{email}"
        self.client.delete(key)
    
    async def update_signup_data(self, email: str, **updates)-> None:
        data = await self.get_signup_data(email)
        if not data:
            return

        #preserve existing ttl for the redis data stored
        key = f"signup:{email}"
        ttl = await self.client.ttl(key)

        if ttl <= 0:
            return

        data.update(updates)
        await self.client.setex(key, ttl, json.dumps(data))


    #token redis implementations
    async def is_token_blacklisted(self, token: str)->bool:
        key=f"blacklist:{token}"
        return await self.client.exists(key) > 0
    
    async def store_blacklisted_token(self, token:str, expiry:int)->None:
        key = f"blacklist{token}"
        await self.client.setex(key, expiry, '1')

 