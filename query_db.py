from typing import List

from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from database import CandidatesDB, SkillsDB, session
from schema import CRUDSkills, RelationshipSkills, AddCandidates, GetCandidate
from custom_exceptions import non_existent_object


async def get_candidates_db(candidate_id_db: int | None = None, lim: int | None = None,
                            page: int | None = None) -> GetCandidate:
    """
    Retrieves data from the database.
    :param candidate_id_db: id of item from database
    :param lim: quantity of objects to return
    :param page: offset in sql request
    :return: GetCandidate
    """

    async with (session() as ses):
        if candidate_id_db:
            query = select(CandidatesDB).where(CandidatesDB.id == candidate_id_db
                                               ).options(selectinload(CandidatesDB.skills))
        else:
            query = select(CandidatesDB).options(selectinload(CandidatesDB.skills)).limit(lim).offset(page * lim)

        response = await ses.execute(query)

    task_set = response.scalars().first()
    print(task_set)
    if not task_set and candidate_id_db:
        non_existent_object()
    elif not task_set:
        non_existent_object(message="at this moment there are no objects in database")

    return task_set


async def add_candidates_db(candidate: AddCandidates):
    """
    Add data to the database.
    :param candidate: class with data to record in database
    """

    async with session() as ses:
        candidate_data = candidate.model_dump()
        skills = candidate_data['skills']
        del candidate_data['skills']
        # print(candidate_data)
        candidate_bd = CandidatesDB(**candidate_data)
        ses.add(candidate_bd)
        await ses.flush()
        # print(candidate_bd.id)
        if skills:
            for i in skills:
                i['candidate_id'] = candidate_bd.id
            await ses.execute(insert(SkillsDB).values(skills))
        # print(skills)
        await ses.commit()


async def update_candidates_db(candidate_id_db: int, values):
    """
    Update data of item from the database.
    :param values: new information to be recorded
    :param candidate_id_db: id of candidate from database
    """
    async with session() as ses:
        await ses.execute(update(CandidatesDB).where(CandidatesDB.id == candidate_id_db).values(values))
        await ses.commit()


async def delete_candidates_db(candidate_id_db: int):
    """
    Delete data from the database.
    :param candidate_id_db: id of candidate from database
    """

    async with session() as ses:
        await ses.execute(delete(CandidatesDB).where(CandidatesDB.id == candidate_id_db))
        await ses.commit()
