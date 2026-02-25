from aiogram import Bot, Dispatcher, types
from app.config import settings
from app.gateway import forward_event
from app.schemas import MessageEvent
from app.security import check_chat_allowed, rate_limit
from app.utils import unix_now, extract_user
import app.state as state

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def handle_message(message: types.Message):
    check_chat_allowed(message.chat.id)
    rate_limit(message.chat.id)

    user = extract_user(message)

    event = MessageEvent(
        event="message",
        chat_id=message.chat.id,
        user_id=user.get("user_id"),
        username=user.get("username"),
        timestamp=unix_now(),
        text=message.text,
        raw=message.model_dump(),
    )

    if settings.QUEUE_BACKEND == "sqlite" and state.queue is not None:
        await state.queue.enqueue(event.model_dump())
    else:
        await forward_event(event)