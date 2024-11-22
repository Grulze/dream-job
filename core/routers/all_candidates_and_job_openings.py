from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from core.db.request_db import get_model_db
from core.db.database import CandidatesDB, JobOpeningsDB
from core.schemas import GetCandidates, GetJobOpenings, Pagination


router = APIRouter(tags=["Get all candidates and job openings"])


@router.get("/candidates", response_model=List[GetCandidates])
@cache(1, namespace="all_candidates_with_pagination")
async def get_all_candidates(pagination: Pagination = Depends()) -> List[GetCandidates]:
    """
    Return all candidates from database with pagination.
    :param pagination: class with information that used for pagination
    :return: List[GetCandidates]
    """
    return await get_model_db(orm_table_class=CandidatesDB, lim=pagination.limit, page=pagination.page)


@router.get("/job-openings", response_model=List[GetJobOpenings])
@cache(1, namespace="all_job_openings_with_pagination")
async def get_job_openings(pagination: Pagination = Depends()) -> List[GetJobOpenings]:
    """
    Return all job openings from database with pagination.
    :param pagination: class with information that used for pagination.
    :return: List[GetCandidates]
    """
    return await get_model_db(orm_table_class=JobOpeningsDB, lim=pagination.limit, page=pagination.page)
