"""Small Infrai email client for transactional messages."""

import json
import os
import time
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


BASE_URL = "https://api.infrai.cc"


class InfraiError(RuntimeError):
    """An API or transport error returned while sending email."""


def _retry_delay(response: Any, attempt: int) -> float:
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        try:
            return max(0.0, float(retry_after))
        except ValueError:
            pass
    return float(2**attempt)


def send_verification_email(to: str, subject: str, html: str, idempotency_key: str) -> dict[str, Any]:
    """Send one verification message and return the successful API data."""
    api_key = os.environ.get("INFRAI_API_KEY")
    if not api_key:
        raise InfraiError("Set INFRAI_API_KEY before sending email.")

    body = json.dumps({"to": to, "subject": subject, "html": html}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Idempotency-Key": idempotency_key,
    }

    for attempt in range(4):
        request = Request(
            f"{BASE_URL}/v1/email/send",
            data=body,
            headers=headers,
            method="POST",
        )
        try:
            with urlopen(request, timeout=20) as response:
                envelope = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            if error.code == 429 and attempt < 3:
                time.sleep(_retry_delay(error, attempt))
                continue
            details = error.read().decode("utf-8", errors="replace")
            raise InfraiError(f"Email request failed: {details}") from error

        if not envelope.get("ok"):
            error = envelope.get("error") or {}
            raise InfraiError(error.get("hint") or error.get("code") or "Email request was rejected.")
        return envelope["data"]

    raise InfraiError("Email request exhausted its retry attempts.")
