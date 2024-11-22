from fastapi import APIRouter
from fastapi_cache.decorator import cache

from core.db.request_db import update_record_db, get_skills_db, delete_required_skill_db
from core.db.database import RequiredSkillsDB
from core.schemas import GetRequiredSkills, PATCHRequiredSkills, AddRequiredSkills
from core.custom_exceptions import invalid_id


router = APIRouter(prefix="/job-openings/skills", tags=["RUD job openings skills"])


@router.get("/{skill_id}", response_model=GetRequiredSkills)
@cache(1, namespace="job_openings_skills")
async def get_skills(skill_id: int) -> GetRequiredSkills:
    """
    Return skill of job opening from database with the transmitted skill id.
    :param skill_id: id of skill in table.
    :return: GetRequiredSkills
    """
    invalid_id(id_number=skill_id)
    return await get_skills_db(orm_table_class=RequiredSkillsDB, skill_id_db=skill_id)


@router.put("/{skill_id}", status_code=204)
async def update_skills(skill_id: int, data: AddRequiredSkills):
    """
    Full update data about job opening skill.
    :param skill_id: id of skill in table.
    :param data: new data about skill.
    """
    invalid_id(id_number=skill_id)
    await update_record_db(record_id_db=skill_id, values=data.dict(exclude_none=True),
                           orm_table_class=RequiredSkillsDB)


@router.patch("/{skill_id}")
async def partial_update_skills(skill_id: int, data: PATCHRequiredSkills) -> GetRequiredSkills:
    """
    Partial update data about job opening skill.
    :param skill_id: id of skill in table.
    :param data: new data about skill.
    :return: GetRequiredSkills
    """
    invalid_id(id_number=skill_id)
    await update_record_db(record_id_db=skill_id, values=data.dict(exclude_none=True),
                           orm_table_class=RequiredSkillsDB)
    return await get_skills_db(orm_table_class=RequiredSkillsDB, skill_id_db=skill_id)


@router.delete("/{skill_id}", status_code=204)
async def delete_skills(skill_id: int):
    """
    Delete skill of job opening from table in database.
    :param skill_id: id of skill in table.
    """
    invalid_id(id_number=skill_id)
    await delete_required_skill_db(record_id_db=skill_id)
