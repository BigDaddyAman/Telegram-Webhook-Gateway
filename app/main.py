from fastapi import FastAPI
from app.config import settings
from app.routers.health import router as health_router
from app.webhook import telegram_webhook

import asyncio
import time
import app.state as state

from app.queue.sqlite import SQLiteQueue
from app.worker import worker_loop
from app import state


app = FastAPI(title="Telegram Webhook Gateway")

app.include_router(health_router)

app.add_api_route(
    settings.TELEGRAM_WEBHOOK_PATH,
    telegram_webhook,
    methods=["POST"],
)


@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "telegram-webhook-gateway",
        "public_mode": settings.PUBLIC_MODE,
    }


@app.on_event("startup")
async def startup():
    if settings.QUEUE_BACKEND == "sqlite":
        state.queue = SQLiteQueue(settings.SQLITE_PATH)
        await state.queue.init()
        asyncio.create_task(worker_loop())  

@app.get("/stats")
async def stats():
    queued = 0

    if state.queue is not None:
        queued = await state.queue.count()

    uptime = int(time.time() - state.started_at)

    return {
        "queued": queued,
        "uptime_sec": uptime,
    }