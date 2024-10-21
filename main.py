from fastapi import FastAPI
from contextlib import asynccontextmanager

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend

from router import CRUDCandidates, RUDCandidatesSkills, CRCandidatesSkills, CRUDJobOpenings, RUDJobOpeningsSkills, \
    CRJobOpeningsSkills, AllCandidatesAndJobOpenings
from database import create_table
# from redis_conf import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create a connection to the cache service and tables in database (if they don't exist).
    Also, when the service is turned off, it sends a message about this.
    """
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    await create_table()

    yield


my_job = FastAPI(openapi_prefix="/api/v1", lifespan=lifespan)

my_job.include_router(AllCandidatesAndJobOpenings.router)
my_job.include_router(CRUDCandidates.router)
my_job.include_router(RUDCandidatesSkills.router)
my_job.include_router(CRCandidatesSkills.router)
my_job.include_router(CRUDJobOpenings.router)
my_job.include_router(RUDJobOpeningsSkills.router)
my_job.include_router(CRJobOpeningsSkills.router)
