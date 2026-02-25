import time
import hmac
import hashlib
from collections import defaultdict
from fastapi import HTTPException
from app.config import settings

def check_chat_allowed(chat_id: int) -> None:
    if settings.PUBLIC_MODE:
        return

    if chat_id not in settings.AUTHORIZED_CHAT_IDS:
        raise HTTPException(status_code=403, detail="Chat not allowed")

_requests: dict[int, list[float]] = defaultdict(list)


def rate_limit(chat_id: int) -> None:
    now = time.time()
    window = 60

    _requests[chat_id] = [
        t for t in _requests[chat_id]
        if now - t < window
    ]

    if len(_requests[chat_id]) >= settings.RATE_LIMIT_PER_MIN:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    _requests[chat_id].append(now)

def sign_payload(payload: bytes, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()