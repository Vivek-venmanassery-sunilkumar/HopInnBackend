from app.core.repositories.traveller.email_repo import EmailRepo


class CeleryEmailRepo(EmailRepo):
    #Adapter that delegates email sending to Celery
    def send(self, email: str, otp: str)-> None:
        from app.infrastructure.task_queues.celery.tasks import send_otp_email
        send_otp_email.delay(email, otp)