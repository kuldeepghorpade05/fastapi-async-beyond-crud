from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from src.celery_tasks import send_email
from src.config import Config

from .dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker, get_current_user
from .schemas import UserCreateModel, UserLoginModel, EmailModel, PasswordResetRequestModel, PasswordResetConfirmModel, UserBooksModel
from .service import UserService
from .utils import create_access_token, verify_password, generate_passwd_hash, create_url_safe_token, decode_url_safe_token
from src.errors import UserAlreadyExists, UserNotFound, InvalidToken, InvalidCredentials

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])
REFRESH_TOKEN_EXPIRY = 2


# =========================
# Test Email Endpoint
# =========================
@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    """
    Test endpoint to send an email using Celery
    """
    recipients = emails.addresses
    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to our app"

    send_email.delay(recipients, subject, html)

    return {"message": "Email sent successfully"}


# =========================
# Signup Endpoint
# =========================
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    # Generate verification token
    token = create_url_safe_token({"email": email})
    link = f"{Config.DOMAIN}/api/v1/auth/verify/{token}"

    # Send verification email asynchronously via Celery
    subject = "Verify Your Email"
    html = f"""
    <h1>Verify your Email</h1>
    <p>Click this link to verify your account:</p>
    <a href="{link}">{link}</a>
    """
    send_email.delay([email], subject, html)

    return {
        "message": "Account created! Verification email sent.",
        "user": new_user,
        "verification_link": link,  # optional, for testing
    }


# =========================
# Email Verification Endpoint
# =========================
@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()

        # Check if already verified
        if user.is_verified:
            return JSONResponse(
                content={"message": "Account already verified"},
                status_code=status.HTTP_200_OK,
            )

        # Update user as verified
        await user_service.update_user(user, {"is_verified": True}, session)

        # Send confirmation email asynchronously via Celery
        subject = "Your Account is Verified!"
        html = f"""
        <h1>Account Verified</h1>
        <p>Hi {user.first_name},</p>
        <p>Your account has been successfully verified. You can now log in!</p>
        """
        send_email.delay([user_email], subject, html)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# =========================
# Login Endpoint
# =========================
@auth_router.post("/login")
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    if user is None:
        raise UserNotFound()

    if not verify_password(password, user.password_hash):
        raise InvalidCredentials()

    if not user.is_verified:
        return JSONResponse(
            content={"message": "Account not verified. Please check your email."},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    access_token = create_access_token({
        "email": user.email,
        "user_uid": str(user.uid),
        "role": user.role,
    })

    refresh_token = create_access_token({
        "email": user.email,
        "user_uid": str(user.uid)
    }, refresh=True, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"email": user.email, "uid": str(user.uid)},
    }


# =========================
# Password Reset Request
# =========================
@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email
    token = create_url_safe_token({"email": email})
    link = f"{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    subject = "Reset Your Password"
    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Click this link to reset your password:</p>
    <a href="{link}">{link}</a>
    """
    send_email.delay([email], subject, html_message)

    return {
        "message": "Password reset email sent! Check your inbox.",
        "reset_link": link,  # optional, for testing
    }


# =========================
# Password Reset Confirmation
# =========================
@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(token: str, passwords: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()

        passwd_hash = generate_passwd_hash(new_password)
        await user_service.update_user(user, {"password_hash": passwd_hash}, session)

        return {"message": "Password reset successfully"}

    raise HTTPException(status_code=500, detail="Error occurred during password reset.")
