import smtplib
from email.message import EmailMessage
from app.config.email_config import email_settings


class SMTPEmail:
    #Concrete implementation using SMTP
    def send(self,email: str, otp: str) -> None:
        msg = EmailMessage()
        msg.set_content(f"Your otp: {otp}")
        msg['Subject'] = "Verification Code"
        msg['From'] = email_settings.FROM_EMAIL
        msg['To'] = email


        with smtplib.SMTP(email_settings.HOST, email_settings.PORT) as server:
            server.starttls()
            server.login(email_settings.USERNAME, email_settings.PASSWORD)
            server.send_message(msg)