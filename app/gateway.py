import logging
import httpx
import json
import hmac
import hashlib

from app.config import settings
from app.schemas import MessageEvent

logger = logging.getLogger("gateway")

_client: httpx.AsyncClient | None = None


async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=settings.FORWARD_TIMEOUT_SEC,
            headers={
                "User-Agent": "telegram-webhook-gateway",
                "Content-Type": "application/json",
            },
        )
    return _client


def sign_payload(payload: bytes, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()


async def forward_event(event: MessageEvent) -> None:
    client = await get_client()

    payload = event.model_dump()
    body = json.dumps(payload).encode()

    headers = {}
    if settings.OUTBOUND_SECRET:
        headers["X-Gateway-Signature"] = sign_payload(
            body, settings.OUTBOUND_SECRET
        )

    failed_targets: list[str] = []

    for url in settings.target_urls:
        try:
            resp = await client.post(
                url,
                content=body,
                headers=headers,
            )
            resp.raise_for_status()
        except Exception:
            logger.exception(f"Failed to forward to {url}")
            failed_targets.append(url)

    if failed_targets:
        raise RuntimeError(
            f"Fan-out failed for {len(failed_targets)} target(s)"
        )