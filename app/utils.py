import time
from aiogram.types import Message


def unix_now() -> int:
    return int(time.time())


def extract_user(message: Message) -> dict:
    if not message.from_user:
        return {}

    return {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "is_bot": message.from_user.is_bot,
    }