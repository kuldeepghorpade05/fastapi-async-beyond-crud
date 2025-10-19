import logging
import uuid
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer

import jwt
from passlib.context import CryptContext

from src.config import Config

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    """
    Generates a bcrypt hash for the password.
    Ensures password is <= 72 bytes (UTF-8 safe).
    """
    truncated_bytes = password.encode("utf-8")[:72]  # keep as bytes
    return passwd_context.hash(truncated_bytes)


def verify_password(password: str, hash: str) -> bool:
    """
    Verifies a password against a bcrypt hash.
    Truncates password to 72 bytes to match hashing.
    """
    truncated_bytes = password.encode("utf-8")[:72]  # keep as bytes
    return passwd_context.verify(truncated_bytes, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {
        "user": user_data,
        "exp": datetime.now()
        + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


serializer = URLSafeTimedSerializer(secret_key=Config.JWT_SECRET, salt="email-configuration")


def create_url_safe_token(data: dict) -> str:
    return serializer.dumps(data)


def decode_url_safe_token(token: str) -> dict:
    try:
        return serializer.loads(token)
    except Exception as e:
        logging.error(str(e))
        return None
