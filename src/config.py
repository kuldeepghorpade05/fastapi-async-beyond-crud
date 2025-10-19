from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # =========================
    # Database
    # =========================
    DATABASE_URL: str

    # =========================
    # JWT Settings
    # =========================
    JWT_SECRET: str
    JWT_ALGORITHM: str

    # =========================
    # Redis / Celery
    # =========================
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL

    # =========================
    # Mail Settings
    # =========================
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # =========================
    # App Domain
    # =========================
    DOMAIN: str

    # =========================
    # Pydantic Config
    # =========================
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# =========================
# Create Config Object
# =========================
Config = Settings()

# =========================
# Celery Variables (for worker)
# =========================
broker_url = Config.CELERY_BROKER_URL
result_backend = Config.CELERY_RESULT_BACKEND
broker_connection_retry_on_startup = True
