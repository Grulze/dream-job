from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from core.db.request_db import add_skills_db, get_skills_db
from core.db.database import RequiredSkillsDB
from core.schemas import GetJobOpeningsRequiredSkills, AddRequiredSkills
from core.custom_exceptions import invalid_id


router = APIRouter(prefix="/job-openings/{job_openings_id}/skills", tags=["CR skills of a certain job opening"])


@router.get("", response_model=List[GetJobOpeningsRequiredSkills])
@cache(1, namespace="all_job_openings_skills")
async def get_skills(job_openings_id: int) -> List[GetJobOpeningsRequiredSkills]:
    """
    Return all skills of job opening from database with the transmitted candidate id.
    :param job_openings_id: id of job opening in database.
    :return: List[GetJobOpeningsRequiredSkills]
    """
    invalid_id(id_number=job_openings_id)
    return await get_skills_db(orm_table_class=RequiredSkillsDB, foreign_key=job_openings_id)


@router.post("", status_code=201)
async def add_skills(job_openings_id: int, skills_data: List[AddRequiredSkills]):
    """
    Creating new skills of job opening.
    :param job_openings_id: id of job opening in database.
    :param skills_data: list with dicts of skills data.
    """
    await add_skills_db(skills=skills_data, orm_table_class=RequiredSkillsDB, foreign_key=job_openings_id)
