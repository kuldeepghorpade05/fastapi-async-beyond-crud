from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config

# =========================
# Mail configuration
# =========================
mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT,            # use Config value instead of hardcoded 587
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    USE_CREDENTIALS=Config.USE_CREDENTIALS,
    VALIDATE_CERTS=Config.VALIDATE_CERTS,
    # TEMPLATE_FOLDER can be added later if needed
)

# =========================
# FastMail instance
# =========================
mail = FastMail(config=mail_config)

# =========================
# Helper function to create message
# =========================
def create_message(recipients: list[str], subject: str, body: str) -> MessageSchema:
    """
    Creates an HTML email message.

    Args:
        recipients (list[str]): List of recipient email addresses.
        subject (str): Email subject.
        body (str): HTML content for the email body.

    Returns:
        MessageSchema: Ready-to-send email object
    """
    return MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
