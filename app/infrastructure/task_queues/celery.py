from celery import Celery
from app.config.redis import redis_settings
from app.infrastructure.repositories import SMTPEmail

celery = Celery(
    'tasks',
    broker = f'redis://{redis_settings.HOST}:{redis_settings.PORT}/{redis_settings.DB}',
    backend = f'redis://{redis_settings.HOST}:{redis_settings.PORT}/{redis_settings.DB}'
)

@celery.task
def send_otp_email(email: str, otp: str):
    email_repo = SMTPEmail()
    email_repo.send(email, otp)