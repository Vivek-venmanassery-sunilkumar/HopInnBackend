import json
import redis
from app.config.redis import redis_settings
from typing import Optional, Dict, Any

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host = redis_settings.HOST,
            port = redis_settings.PORT,
            db = redis_settings.DB,
            password = redis_settings.PASSWORD or None,
            decode_responses= True,
            socket_connect_timeout = 5,
            )
    
    async def store_signup_data(self, email: str, otp: str, user_data: dict) ->None:
        key = f"signup:{email}"
        data = {
            "otp": otp,
            "user_data": user_data,
            "attempts": 0
        }
        self.client.setex(
            name=key,
            time=redis_settings.OTP_EXPIRE_SECONDS,
            value = json.dumps(data)
        )
    
    async def verify_otp_and_retrieve_data(self, email: str, otp: str)->Optional[Dict[str, Any]]:
        key = f"signup:{email}"
        data = self.client.get(key)

        if not data:
            return None
        
        parsed = json.loads(data)

        if parsed["attempts"] >= redis_settings.MAX_OTP_ATTEMPTS:
            self.client.delete(key)
            return None
        
        if parsed["otp"] != otp:
            parsed["attempts"] += 1
            self.client.setex(
                name=key,
                time=redis_settings.OTP_EXPIRE_SECONDS,
                value = json.dumps(parsed)
            )
            return None
        self.client.delete(key)
        return parsed["user_data"]