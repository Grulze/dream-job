from fastapi import APIRouter
from fastapi_cache.decorator import cache

from core.db.request_db import add_model_db, delete_record_db, get_model_db, update_record_db
from core.db.database import CandidatesDB, CandidatesSkillsDB
from core.schemas import AddCandidates, Candidates, PATCHCandidates, GetCandidates
from core.custom_exceptions import invalid_id


router = APIRouter(prefix="/candidates", tags=["CRUD candidates"])


@router.get("/{candidate_id}", response_model=GetCandidates)
@cache(1, namespace="candidates")
async def get_candidates(candidate_id: int) -> GetCandidates:
    """
    Return candidate from database with the transmitted id.
    :param candidate_id: id of candidate being searched for.
    :return: GetCandidates
    """
    invalid_id(id_number=candidate_id)
    return await get_model_db(orm_table_class=CandidatesDB, record_id_db=candidate_id)


@router.post("", status_code=201)
async def add_candidates(candidate_data: AddCandidates):
    """
    Creating new candidate.
    :param candidate_data: data about candidate.
    """
    await add_model_db(
        model=candidate_data, orm_table_class=CandidatesDB, foreign_orm_table_class=CandidatesSkillsDB
    )


@router.put("/{candidate_id}", status_code=204)
async def update_candidates(candidate_id: int, data: Candidates):
    """
    Full update data about candidate.
    :param candidate_id: id of candidate in table.
    :param data: new data about candidate.
    """
    invalid_id(id_number=candidate_id)
    await update_record_db(record_id_db=candidate_id, values=data.dict(), orm_table_class=CandidatesDB)


@router.patch("/{candidate_id}")
async def partial_update_candidates(candidate_id: int, data: PATCHCandidates) -> GetCandidates:
    """
    Partial update data about candidate.
    :param candidate_id: id of candidate in table.
    :param data: new data about candidate.
    :return: GetCandidates
    """
    invalid_id(id_number=candidate_id)
    await update_record_db(record_id_db=candidate_id, values=data.dict(exclude_none=True),
                           orm_table_class=CandidatesDB)
    return await get_model_db(orm_table_class=CandidatesDB, record_id_db=candidate_id)


@router.delete("/{candidate_id}", status_code=204)
async def delete_candidates(candidate_id: int):
    """
    Delete candidate from table in database.
    :param candidate_id: id of candidate in table.
    """
    invalid_id(id_number=candidate_id)
    await delete_record_db(record_id_db=candidate_id, orm_table_class=CandidatesDB)
