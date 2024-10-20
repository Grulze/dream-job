from fastapi import FastAPI
from contextlib import asynccontextmanager

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend

from router import crud_candidates, crud_skills
# from database import create_table
# from redis_conf import redis


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Create a connection to the cache service and tables in database (if they don't exist).
#     Also, when the service is turned off, it sends a message about this.
#     """
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#
#     await create_table()
#
#     yield


my_shop = FastAPI()#lifespan=lifespan)
my_shop.include_router(crud_candidates)
my_shop.include_router(crud_skills)
