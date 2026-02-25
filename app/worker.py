import asyncio
import app.state as state
from app.gateway import forward_event
from app.schemas import MessageEvent
from app.config import settings

async def worker_loop():
    print("🟢 WORKER STARTED")

    while True:
        if state.queue is None:
            await asyncio.sleep(0.5)
            continue

        job = await state.queue.fetch_next()
        if not job:
            await asyncio.sleep(0.5)
            continue

        event_id, payload, attempts = job

        if attempts > 0:
            delay = settings.BASE_RETRY_DELAY_SEC * (2 ** (attempts - 1))
            await asyncio.sleep(delay)

        try:
            event = MessageEvent(**payload)
            await forward_event(event)

            await state.queue.delete(event_id)
            print(f"✅ Sent event {event_id}")

        except Exception as e:
            if attempts + 1 >= settings.MAX_RETRIES:
                await state.queue.delete(event_id)
                print(f"❌ Dropped event {event_id} after retries")
            else:
                await state.queue.increment_attempts(event_id)
                print(f"🔁 Retry {attempts + 1} for event {event_id}")

        await asyncio.sleep(0)