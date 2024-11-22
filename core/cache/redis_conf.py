from redis import asyncio as aioredis
from core.config import REDIS_HOST, REDIS_PORT


redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
