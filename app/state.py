from typing import Optional
from app.queue.sqlite import SQLiteQueue
import time

queue: Optional[SQLiteQueue] = None
started_at: float = time.time()