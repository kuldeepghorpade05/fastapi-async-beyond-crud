from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync
from src.config import Config

# =========================
# Celery app configuration
# =========================
c_app = Celery(
    "worker",
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL,
)

c_app.conf.broker_connection_retry_on_startup = True

# =========================
# Celery task to send email
# =========================
@c_app.task
def send_email(recipients: list[str], subject: str, body: str):
    """
    Sends an email asynchronously using Celery and FastAPI-Mail.

    Args:
        recipients (list[str]): List of recipient email addresses.
        subject (str): Email subject.
        body (str): HTML email body.
    """
    message = create_message(recipients=recipients, subject=subject, body=body)

    # Use async_to_sync to call async FastMail in a sync Celery task
    async_to_sync(mail.send_message)(message)

    print(f"✅ Email sent to {recipients}")
