from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from core.db.request_db import find_suitable_records
from core.db.database import CandidatesDB, JobOpeningsDB
from core.schemas import GetCandidates, GetJobOpenings, Pagination, Sorting
from core.custom_exceptions import invalid_id

router = APIRouter(prefix="", tags=["Selection of candidates and job openings"])


@router.get("/job-openings/{job_id}/selection", response_model=List[GetCandidates])
@cache(1, namespace="job_openings_selection")
async def get_suitable_candidates(job_id: int, pagination: Pagination = Depends(),
                                  sorting_param: Sorting = Depends()) -> List[GetCandidates]:
    """
    Return all suitable candidates from database with pagination.
    :param job_id: id of the job openings being searched for.
    :param pagination: class with information that used for pagination.
    :param sorting_param: parameter by which sorting will be performed, 'lower' - from less qualified,
    'upper' - from more qualified.
    :return: List[GetCandidates]
    """
    invalid_id(job_id)
    return await find_suitable_records(
        record_id=job_id, orm_table_for_search=CandidatesDB, lim=pagination.limit, page=pagination.page,
        sorting=sorting_param.sorting_from.value
    )


@router.get("/candidates/{candidate_id}/selection", response_model=List[GetJobOpenings])
@cache(1, namespace="candidates_selection")
async def get_suitable_job_openings(candidate_id: int, pagination: Pagination = Depends(),
                                    sorting_param: Sorting = Depends()) -> List[GetJobOpenings]:
    """
    Return all suitable job openings from database with pagination.
    :param candidate_id: id of the candidates being searched for.
    :param pagination: class with information that used for pagination.
    :param sorting_param: parameter by which sorting will be performed, 'lower' - from less qualified,
    'upper' - from more qualified.
    :return: List[GetJobOpenings]
    """
    invalid_id(candidate_id)
    return await find_suitable_records(
        record_id=candidate_id, orm_table_for_search=JobOpeningsDB, lim=pagination.limit, page=pagination.page,
        sorting=sorting_param.sorting_from.value
    )
