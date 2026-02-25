from typing import Set
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., description="Telegram bot token")
    TELEGRAM_WEBHOOK_PATH: str = "/telegram/webhook"
    TELEGRAM_SECRET_TOKEN: str | None = None

    TARGET_WEBHOOK_URL: str | None = Field(
        None, description="Default webhook target"
    )

    TARGET_WEBHOOK_URLS: str | None = None

    PUBLIC_MODE: bool = False
    AUTHORIZED_CHAT_IDS: Set[int] = set()
    RATE_LIMIT_PER_MIN: int = 30
    MAX_BODY_SIZE_KB: int = 512

    FORWARD_TIMEOUT_SEC: int = 10

    QUEUE_BACKEND: str = "sqlite"
    SQLITE_PATH: str = "./events.db"

    MAX_RETRIES: int = 5
    BASE_RETRY_DELAY_SEC: int = 2

    OUTBOUND_SECRET: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    @validator("AUTHORIZED_CHAT_IDS", pre=True)
    def parse_chat_ids(cls, v):
        if not v:
            return set()
        if isinstance(v, set):
            return v
        return {int(x.strip()) for x in str(v).split(",")}

    @property
    def target_urls(self) -> list[str]:
        """
        Fan-out logic:
        - If TARGET_WEBHOOK_URLS is set → use multiple
        - Else → fallback to TARGET_WEBHOOK_URL
        """
        if self.TARGET_WEBHOOK_URLS:
            return [
                u.strip()
                for u in self.TARGET_WEBHOOK_URLS.split(",")
                if u.strip()
            ]
        return [self.TARGET_WEBHOOK_URL]


settings = Settings()