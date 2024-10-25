from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from router import CRUDCandidates, RUDCandidatesSkills, CRCandidatesSkills, CRUDJobOpenings, RUDJobOpeningsSkills, \
    CRJobOpeningsSkills, AllCandidatesAndJobOpenings, SelectionOfCandidatesAndJobOpenings
from create_tables import create_if_the_database_is_empty
from redis_conf import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create a connection to the cache service and tables in database (if they don't exist).
    """
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_if_the_database_is_empty()
    yield


my_job = FastAPI(openapi_prefix="/api/v1", lifespan=lifespan)

my_job.include_router(SelectionOfCandidatesAndJobOpenings.router)
my_job.include_router(AllCandidatesAndJobOpenings.router)
my_job.include_router(CRUDCandidates.router)
my_job.include_router(RUDCandidatesSkills.router)
my_job.include_router(CRCandidatesSkills.router)
my_job.include_router(CRUDJobOpenings.router)
my_job.include_router(RUDJobOpeningsSkills.router)
my_job.include_router(CRJobOpeningsSkills.router)
