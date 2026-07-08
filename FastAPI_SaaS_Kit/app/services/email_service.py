import resend
from app.config import get_settings


def send_welcome_email(to: str, name: str) -> None:
    settings = get_settings()
    if not settings.resend_api_key:
        return
    resend.api_key = settings.resend_api_key
    resend.Emails.send({
        "from": settings.email_from,
        "to": to,
        "subject": f"Welcome to {settings.app_name}!",
        "html": f"<p>Hi {name},</p><p>Welcome aboard! Your account is ready.</p>",
    })


def send_password_reset_email(to: str, reset_url: str) -> None:
    settings = get_settings()
    if not settings.resend_api_key:
        return
    resend.api_key = settings.resend_api_key
    resend.Emails.send({
        "from": settings.email_from,
        "to": to,
        "subject": "Password Reset Request",
        "html": f'<p>Click <a href="{reset_url}">here</a> to reset your password. Link expires in 1 hour.</p>',
    })
