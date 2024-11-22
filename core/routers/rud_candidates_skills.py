from fastapi import APIRouter
from fastapi_cache.decorator import cache

from core.db.request_db import delete_record_db, update_record_db, get_skills_db
from core.db.database import CandidatesSkillsDB
from core.schemas import GetCandidateSkills, PATCHCandidateSkills, AddCandidateSkills
from core.custom_exceptions import invalid_id


router = APIRouter(prefix="/candidates/skills", tags=["RUD candidates skills"])


@router.get("/{skill_id}", response_model=GetCandidateSkills)
@cache(1, namespace="candidates_skills")
async def get_skills(skill_id: int) -> GetCandidateSkills:
    """
    Return skill of candidate from database with the transmitted skill id.
    :param skill_id: id of skill in table.
    :return: GetCandidateSkills
    """
    invalid_id(id_number=skill_id)
    return await get_skills_db(orm_table_class=CandidatesSkillsDB, skill_id_db=skill_id)


@router.put("/{skill_id}", status_code=204)
async def update_skills(skill_id: int, data: AddCandidateSkills):
    """
    Full update data about candidate skill.
    :param skill_id: id of skill in table.
    :param data: new data about skill.
    """
    invalid_id(id_number=skill_id)
    await update_record_db(
        record_id_db=skill_id, values=data.dict(exclude_none=True), orm_table_class=CandidatesSkillsDB
    )


@router.patch("/{skill_id}")
async def partial_update_skills(skill_id: int, data: PATCHCandidateSkills) -> GetCandidateSkills:
    """
    Partial update data about candidate skill.
    :param skill_id: id of skill in table.
    :param data: new data about skill.
    :return: GetCandidateSkills
    """
    invalid_id(id_number=skill_id)
    await update_record_db(
        record_id_db=skill_id, values=data.dict(exclude_none=True), orm_table_class=CandidatesSkillsDB
    )
    return await get_skills_db(orm_table_class=CandidatesSkillsDB, skill_id_db=skill_id)


@router.delete("/{skill_id}", status_code=204)
async def delete_skills(skill_id: int):
    """
    Delete skill of candidate from table in database.
    :param skill_id: id of skill in table.
    """
    invalid_id(id_number=skill_id)
    await delete_record_db(record_id_db=skill_id, orm_table_class=CandidatesSkillsDB)