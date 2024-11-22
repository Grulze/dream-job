from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from core.db.request_db import add_skills_db, get_skills_db
from core.db.database import CandidatesSkillsDB
from core.schemas import GetAllCandidateSkills, AddCandidateSkills
from core.custom_exceptions import invalid_id


router = APIRouter(prefix="/candidates/{candidate_id}/skills", tags=["CR skills of a certain candidate"])


@router.get("", response_model=List[GetAllCandidateSkills])
@cache(1, namespace="all_candidates_skills")
async def get_skills(candidate_id: int) -> List[GetAllCandidateSkills]:
    """
    Return all skills of candidate from database with the transmitted candidate id.
    :param candidate_id: id of candidate in table.
    :return: List[GetAllCandidateSkills]
    """
    invalid_id(id_number=candidate_id)
    return await get_skills_db(orm_table_class=CandidatesSkillsDB, foreign_key=candidate_id)


@router.post("", status_code=201)
async def add_skills(candidate_id: int, skills_data: List[AddCandidateSkills]):
    """
    Creating new skills of candidate.
    :param candidate_id: id of candidate in table.
    :param skills_data: list with dicts of skills data.
    """
    await add_skills_db(skills=skills_data, orm_table_class=CandidatesSkillsDB, foreign_key=candidate_id)
