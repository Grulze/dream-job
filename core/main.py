from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from core.routers import routers_set
from core.db.create_tables import create_if_the_database_is_empty
from core.cache.redis_conf import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create a connection to the cache service and tables in database (if they don't exist).
    """
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_if_the_database_is_empty()
    yield


my_job = FastAPI(openapi_prefix="/api/v1", lifespan=lifespan)

for router in routers_set:
    my_job.include_router(router)
