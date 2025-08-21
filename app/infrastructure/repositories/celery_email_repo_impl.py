from app.core.repositories import EmailRepo


class CeleryEmailRepo(EmailRepo):
    #Adapter that delegates email sending to Celery
    def send(self, email: str, otp: str)-> None:
        from app.infrastructure.task_queues.celery import send_otp_email
        send_otp_email.delay(email, otp)