from typing import List, Type

from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert, func, desc, asc
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from database import CandidatesDB, CandidatesSkillsDB, session, Base, JobOpeningsDB, RequiredSkillsDB
from schema import GetCandidateSkills, GetCandidates, GetJobOpenings, GetRequiredSkills
from custom_exceptions import non_existent_object, non_existing_foreign_key


async def get_model_db(orm_table_class: Type[Base], record_id_db: int | None = None, lim: int | None = None,
                       page: int | None = None) -> List | GetJobOpenings | GetCandidates:
    """
    Retrieves data from the database.
    :param orm_table_class: table from database.
    :param record_id_db: id of record from database.
    :param lim: quantity of objects to return.
    :param page: offset in sql request.
    :return: List
    """
    async with session() as ses:
        if record_id_db:
            query = select(orm_table_class).where(orm_table_class.id == record_id_db).options(
                selectinload(orm_table_class.skills))
        else:
            query = select(orm_table_class).options(selectinload(orm_table_class.skills)
                                                    ).limit(lim).offset(page * lim)
        response = await ses.execute(query)
    records_set = response.scalars().first() if record_id_db else response.scalars().all()

    if not records_set and record_id_db:
        non_existent_object()
    elif not records_set:
        non_existent_object(message="at this moment there are no objects in database")

    return records_set


async def get_skills_db(orm_table_class: Type[Base], skill_id_db: int | None = None,
                        foreign_key: int | None = None) -> List | GetCandidateSkills | GetRequiredSkills:
    """
    Retrieves data from the database.
    :param orm_table_class: table from database.
    :param skill_id_db: id of skill from database.
    :param foreign_key: ForeignKey from table.
    :return: List
    """
    async with session() as ses:
        if foreign_key:
            query = select(orm_table_class).where(orm_table_class.foreign_key == foreign_key)
        else:
            query = select(orm_table_class).where(orm_table_class.id == skill_id_db)
        response = await ses.execute(query)
    records_set = response.scalars().first() if skill_id_db else response.scalars().all()

    if not records_set and skill_id_db:
        non_existent_object()
    elif not records_set:
        non_existent_object(message="at this moment there are no objects in database")

    return records_set


async def add_model_db(model: BaseModel, orm_table_class: Type[Base], foreign_orm_table_class: Type[Base]):
    """
    Add data to the database.
    :param model: model with data to record in database.
    :param orm_table_class: table from database.
    :param foreign_orm_table_class: related table from database.
    """
    model_data = model.model_dump()
    print(model_data)
    async with session() as ses:
        skills = model_data['skills']
        print(skills)
        del model_data['skills']
        data_bd = orm_table_class(**model_data)
        ses.add(data_bd)
        await ses.flush()
        if skills:
            for skill in skills:
                skill['foreign_key'] = data_bd.id
            await ses.execute(insert(foreign_orm_table_class).values(skills))
        await ses.commit()


async def add_skills_db(skills: List[BaseModel], orm_table_class: Type[Base], foreign_key: int):
    """
    Add skills to the database.
    :param skills: list with skills to record in database.
    :param orm_table_class: table from database.
    :param foreign_key: ForeignKey from table.
    """
    async with (session() as ses):
        data = []
        for i in skills:
            skill = i.model_dump()
            skill['foreign_key'] = foreign_key
            data.append(skill)
        try:
            await ses.execute(insert(orm_table_class).values(data))
        except IntegrityError:
            non_existing_foreign_key()
        finally:
            if orm_table_class is RequiredSkillsDB:
                await ses.execute(update(JobOpeningsDB).where(JobOpeningsDB.id == foreign_key)
                                  .values(skills_quantity=JobOpeningsDB.skills_quantity + len(data)))
        await ses.commit()


async def update_record_db(record_id_db: int, values: dict, orm_table_class: Type[Base]):
    """
    Update data of item from the database.
    :param values: new information to be recorded
    :param record_id_db: id of record from database
    :param orm_table_class: table from database
    """
    async with session() as ses:
        await ses.execute(update(orm_table_class).where(orm_table_class.id == record_id_db).values(values))
        await ses.commit()


async def delete_record_db(record_id_db: int, orm_table_class: Type[Base]):
    """
    Delete data from the database.
    :param record_id_db: id of record from the database
    :param orm_table_class: table from database
    """
    async with session() as ses:
        if orm_table_class is RequiredSkillsDB:
            job_id = await ses.execute(select(RequiredSkillsDB.foreign_key).where(orm_table_class.id == record_id_db))
            if job_id:
                ses.execute(update(JobOpeningsDB).where(JobOpeningsDB.id == job_id)
                            .values(skills_quantity=JobOpeningsDB.skills_quantity - 1))

        await ses.execute(delete(orm_table_class).where(orm_table_class.id == record_id_db))
        await ses.commit()


async def delete_required_skill_db(record_id_db: int):
    """
    Delete skill from the table required_skills.
    :param record_id_db: id of record from the table required_skills
    """
    async with session() as ses:
        job_id = await ses.execute(select(RequiredSkillsDB.foreign_key).where(RequiredSkillsDB.id == record_id_db))
        job_id = job_id.one_or_none()
        if job_id:
            await ses.execute(update(JobOpeningsDB).where(JobOpeningsDB.id == job_id[0])
                              .values(skills_quantity=JobOpeningsDB.skills_quantity - 1))
            await ses.execute(delete(RequiredSkillsDB).where(RequiredSkillsDB.id == record_id_db))
        await ses.commit()


async def find_suitable_records(
        record_id: int, orm_table_for_search: Type[CandidatesDB | JobOpeningsDB], sorting, lim: int, page: int) -> List:
    """
    Selection of relevant candidates or job openings.
    :param record_id: id of record for which the selection will be made.
    :param orm_table_for_search: the table with the record to be searched for.
    :param sorting: sorting parameter.
    :param lim: maximum number of records to be given.
    :param page: group of records (sql offset - lim * page)
    :return: List
    """
    find_candidate_request = (
        select(CandidatesDB, func.sum(CandidatesSkillsDB.score).label('total_score'))
        .join(CandidatesSkillsDB)
        .join(RequiredSkillsDB, RequiredSkillsDB.indexing_skill_name == CandidatesSkillsDB.indexing_skill_name)
        .where(
            RequiredSkillsDB.foreign_key == record_id,
            CandidatesSkillsDB.level >= RequiredSkillsDB.level,
            CandidatesSkillsDB.years_of_experience >= RequiredSkillsDB.years_of_experience
        )
        .group_by(CandidatesDB.id)
        .having(
            func.count(CandidatesSkillsDB.skill_name) == select(JobOpeningsDB.skills_quantity)
            .where(JobOpeningsDB.id == record_id)
        )
        .order_by(asc('total_score') if sorting == 'lower' else desc('total_score'))
    ).options(selectinload(CandidatesDB.skills)).limit(lim).offset(page * lim)

    find_job_openings_request = (
        select(JobOpeningsDB, func.sum(RequiredSkillsDB.score).label('total_score'))
        .join(RequiredSkillsDB)
        .join(CandidatesSkillsDB, RequiredSkillsDB.indexing_skill_name == CandidatesSkillsDB.indexing_skill_name)
        .where(
            CandidatesSkillsDB.foreign_key == record_id,
            RequiredSkillsDB.level <= CandidatesSkillsDB.level,
            RequiredSkillsDB.years_of_experience <= CandidatesSkillsDB.years_of_experience
        )
        .group_by(JobOpeningsDB.id)
        .having(
            func.count(CandidatesSkillsDB.skill_name) == select(JobOpeningsDB.skills_quantity)
            .where(JobOpeningsDB.id == record_id)
        ).order_by(asc('total_score') if sorting == 'lower' else desc('total_score'))
    ).options(selectinload(JobOpeningsDB.skills)).limit(lim).offset(page * lim)

    async with session() as ses:
        response = await ses.execute(
            find_candidate_request if orm_table_for_search is CandidatesDB else find_job_openings_request
        )
    records_set = response.scalars().all()
    if not records_set:
        non_existent_object(message="at this moment there are no relevant objects according to these conditions")
    return records_set
