import aiosqlite
import json
import time
import os
from typing import Optional, Tuple


class SQLiteQueue:
    def __init__(self, path: str):
        self.path = path

    async def init(self):
        dir_path = os.path.dirname(self.path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        async with aiosqlite.connect(self.path) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL,
                attempts INTEGER DEFAULT 0,
                created_at INTEGER
            )
            """)
            await db.commit()

    async def enqueue(self, payload: dict):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO events (payload, created_at) VALUES (?, ?)",
                (json.dumps(payload), int(time.time()))
            )
            await db.commit()

    async def fetch_next(self) -> Optional[Tuple[int, dict, int]]:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute("""
                SELECT id, payload, attempts
                FROM events
                ORDER BY id
                LIMIT 1
                """)
            row = await cursor.fetchone()
            if not row:
                return None
            return row[0], json.loads(row[1]), row[2]
        
    async def count(self) -> int:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM events")
            row = await cursor.fetchone()
            return row[0]
        
    async def increment_attempts(self, event_id: int):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "UPDATE events SET attempts = attempts + 1 WHERE id = ?",
                (event_id,))
            await db.commit()

    async def delete(self, event_id: int):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "DELETE FROM events WHERE id = ?",
                (event_id,))
            await db.commit()