from typing import Optional, Literal, Dict, Any
from pydantic import BaseModel


class BaseEvent(BaseModel):
    event: Literal["message"]
    platform: Literal["telegram"] = "telegram"
    chat_id: int
    user_id: Optional[int] = None
    username: Optional[str] = None
    timestamp: int


class MessageEvent(BaseEvent):
    text: Optional[str] = None
    raw: Dict[str, Any] 