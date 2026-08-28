"""Verification-link email content for a marketplace signup."""

from html import escape
from urllib.parse import urlencode
from uuid import uuid4

from .infrai_email import send_verification_email


def send_signup_verification(email: str, app_url: str) -> dict[str, str]:
    """Create and send a confirmation link for one marketplace account."""
    token = uuid4().hex
    query = urlencode({"email": email, "token": token})
    verification_url = f"{app_url.rstrip('/')}/verify-email?{query}"
    safe_url = escape(verification_url, quote=True)
    html = (
        "<h1>Confirm your email</h1>"
        "<p>Finish creating your marketplace account by confirming this address.</p>"
        f'<p><a href="{safe_url}">Confirm email address</a></p>'
    )
    result = send_verification_email(
        to=email,
        subject="Confirm your marketplace email",
        html=html,
        idempotency_key=f"marketplace-signup-{token}",
    )
    return {"message_id": result["message_id"], "verification_url": verification_url}
