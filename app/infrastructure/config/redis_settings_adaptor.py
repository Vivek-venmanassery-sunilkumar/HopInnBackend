from app.core.entities import RedisSettingsEntity
from app.config.redis import redis_settings as infra_redis_settings


def get_core_redis_settings()->RedisSettingsEntity:
    return RedisSettingsEntity(
        HOST=infra_redis_settings.HOST,
        PORT=infra_redis_settings.PORT,
        DB=infra_redis_settings.DB,
        PASSWORD=infra_redis_settings.PASSWORD,
        OTP_EXPIRE_SECONDS=infra_redis_settings.OTP_EXPIRE_SECONDS,
        MAX_OTP_ATTEMPTS=infra_redis_settings.MAX_OTP_ATTEMPTS,
        MAX_OTP_RETRY_ATTEMPTS=infra_redis_settings.MAX_OTP_RETRY_ATTEMPTS
    )