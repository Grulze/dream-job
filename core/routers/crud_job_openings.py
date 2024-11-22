from fastapi import APIRouter
from fastapi_cache.decorator import cache

from core.db.request_db import add_model_db, delete_record_db, get_model_db, update_record_db
from core.db.database import JobOpeningsDB, RequiredSkillsDB
from core.schemas import GetJobOpenings, AddJobOpenings, JobOpenings, PATCHJobOpenings
from core.custom_exceptions import invalid_id


router = APIRouter(prefix="/job-openings", tags=["CRUD job openings"])


@router.get("/{job_openings_id}", response_model=GetJobOpenings)
@cache(1, namespace="job_openings")
async def get_job_openings(job_openings_id: int) -> GetJobOpenings:
    """
    Return job opening from database with the transmitted id.
    :param job_openings_id: id of job opening in database.
    :return: GetJobOpenings
    """
    invalid_id(id_number=job_openings_id)
    return await get_model_db(orm_table_class=JobOpeningsDB, record_id_db=job_openings_id)


@router.post("", status_code=201)
async def add_job_openings(candidate_data: AddJobOpenings):
    """
    Creating new job opening.
    :param candidate_data: data about job opening.
    """
    await add_model_db(model=candidate_data, orm_table_class=JobOpeningsDB,
                       foreign_orm_table_class=RequiredSkillsDB)


@router.put("/{job_openings_id}", status_code=204)
async def update_job_openings(job_openings_id: int, data: JobOpenings):
    """
    Full update data about job opening.
    :param job_openings_id: id of job opening in database.
    :param data: new data about job opening.
    """
    invalid_id(id_number=job_openings_id)
    await update_record_db(record_id_db=job_openings_id, values=data.dict(), orm_table_class=JobOpeningsDB)


@router.patch("/{job_openings_id}")
async def partial_update_job_openings(job_openings_id: int, data: PATCHJobOpenings) -> GetJobOpenings:
    """
    Partial update data about job opening.
    :param job_openings_id: id of job opening in database.
    :param data: new data about job opening.
    :return: GetJobOpenings
    """
    invalid_id(id_number=job_openings_id)
    await update_record_db(record_id_db=job_openings_id, values=data.dict(exclude_none=True),
                           orm_table_class=JobOpeningsDB)
    return await get_model_db(orm_table_class=JobOpeningsDB, record_id_db=job_openings_id)


@router.delete("/{job_openings_id}", status_code=204)
async def delete_job_openings(job_openings_id: int):
    """
    Delete job opening from table in database.
    :param job_openings_id: id of job opening in database.
    """
    invalid_id(id_number=job_openings_id)
    await delete_record_db(record_id_db=job_openings_id, orm_table_class=JobOpeningsDB)
