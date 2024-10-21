from typing import List, Type

from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from database import CandidatesDB, SkillsDB, session, Base, JobOpeningsDB
from schema import Skills, GetSkills, AddCandidates, GetCandidates, AddJobOpenings
from custom_exceptions import non_existent_object, non_existing_foreign_key


async def get_records_db(orm_table_class: Type[Base], record_id_db: int | None = None,
                        foreign_key: int | None = None, lim: int | None = None, page: int | None = None) -> List:
    """
    Retrieves data from the database.
    :param orm_table_class: table from database
    :param record_id_db: id of record from database
    :param foreign_key: ForeignKey from table
    :param lim: quantity of objects to return
    :param page: offset in sql request
    :return: List
    """
    async with (session() as ses):
        if orm_table_class in (CandidatesDB, JobOpeningsDB):
            if record_id_db:
                query = select(orm_table_class).where(orm_table_class.id == record_id_db).options(
                    selectinload(orm_table_class.skills))
            else:
                query = select(orm_table_class).options(selectinload(orm_table_class.skills)
                                                        ).limit(lim).offset(page * lim)
        elif foreign_key:
            query = select(orm_table_class).where(orm_table_class.foreign_key == foreign_key)
        else:
            query = select(orm_table_class).where(orm_table_class.id == record_id_db)
        response = await ses.execute(query)

    records_set = response.scalars().all()
    if not records_set and (record_id_db or foreign_key):
        non_existent_object()
    elif not records_set:
        non_existent_object(message="at this moment there are no objects in database")

    return records_set


async def add_record_db(model: BaseModel, orm_table_class: Type[Base], foreign_key: int | None = None,
                        foreign_orm_table_class: Type[Base] | None = None):
    """
    Add data to the database.
    :param model: model with data to record in database
    :param orm_table_class: table from database
    :param foreign_orm_table_class: related table from database
    :param foreign_key: ForeignKey from table
    """
    model_data = model.model_dump()
    async with session() as ses:
        if type(model) in (AddCandidates, AddJobOpenings):
            skills = model_data['skills']
            del model_data['skills']
            data_bd = orm_table_class(**model_data)
            ses.add(data_bd)
            await ses.flush()
            if skills:
                for i in skills:
                    i['foreign_key'] = data_bd.id
                await ses.execute(insert(foreign_orm_table_class).values(skills))
        elif foreign_key:
            model_data['foreign_key'] = foreign_key
            add_skill_bd = orm_table_class(**model_data)
            ses.add(add_skill_bd)
        else:
            add_record_bd = orm_table_class(**model_data)
            ses.add(add_record_bd)
        try:
            await ses.commit()
        except IntegrityError:
            non_existing_foreign_key()


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
    :param record_id_db: id of record from database
    :param orm_table_class: table from database
    """

    async with session() as ses:
        await ses.execute(delete(orm_table_class).where(orm_table_class.id == record_id_db))
        await ses.commit()
