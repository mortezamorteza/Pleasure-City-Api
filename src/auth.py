import secrets
import hashlib
from datetime import datetime, timezone


def generate_token():
    """
    ساخت توکن تصادفی امن
    """

    return secrets.token_urlsafe(32)


def hash_token(token: str):
    """
    هش کردن توکن برای ذخیره امن
    """

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def generate_user_id():
    """
    ساخت شناسه اختصاصی کاربر
    """

    return "PC-" + secrets.token_hex(8).upper()


def current_time():
    """
    زمان فعلی UTC
    """

    return datetime.now(
        timezone.utc
    ).isoformat()
