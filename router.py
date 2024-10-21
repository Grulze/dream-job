from typing import List

from fastapi import APIRouter, Depends
# from fastapi_cache.decorator import cache

from query_db import add_record_db, delete_record_db, get_records_db, update_record_db
from database import CandidatesDB, SkillsDB, JobOpeningsDB, RequiredSkillsDB
from schema import Skills, GetSkills, AddCandidates, Candidates, PATCHCandidates, GetCandidates, PATCHSkills, \
    GetCandidatesSkills, GetJobOpenings, AddJobOpenings, JobOpenings, PATCHJobOpenings, GetRequiredSkills, \
    RequiredSkills, PATCHRequiredSkills, GetJobOpeningsRequiredSkills, Pagination
from custom_exceptions import invalid_id

# from redis_conf import check_cache_memory, clear_cache_on_update


class SelectionOfCandidatesAndJobOpenings:
    router = APIRouter(prefix="/selection", tags=["Selection of candidates and job openings"])

    @staticmethod
    @router.get("/by-job-openings")
    async def get_all_candidates(pagination: Pagination = Depends()) -> List[GetCandidates]:
        """
        Return all items from database with pagination.
        :param pagination: class with information that used for pagination
        :return: List[GetCandidates]
        """

        return await get_records_db(orm_table_class=CandidatesDB, lim=pagination.limit, page=pagination.page)


class AllCandidatesAndJobOpenings:
    router = APIRouter(tags=["Get all candidates and job openings"])

    @staticmethod
    @router.get("/candidates")
    async def get_all_candidates(pagination: Pagination = Depends()) -> List[GetCandidates]:
        """
        Return all items from database with pagination.
        :param pagination: class with information that used for pagination
        :return: List[GetCandidates]
        """

        return await get_records_db(orm_table_class=CandidatesDB, lim=pagination.limit, page=pagination.page)

    @staticmethod
    @router.get("/job-openings")
    async def get_job_openings(pagination: Pagination = Depends()) -> List[GetJobOpenings]:
        """
        Return all items from database with pagination.
        :param pagination: class with information that used for pagination
        :return: List[GetCandidates]
        """
        return await get_records_db(orm_table_class=JobOpeningsDB, lim=pagination.limit, page=pagination.page)


class CRUDCandidates:
    router = APIRouter(prefix="/candidates", tags=["CRUD candidates"])

    @staticmethod
    @router.get("/{candidate_id}")
    async def get_candidates(candidate_id: int) -> GetCandidates:
        invalid_id(id_number=candidate_id)
        return (await get_records_db(orm_table_class=CandidatesDB, record_id_db=candidate_id))[0]

    @staticmethod
    @router.post("", status_code=201)
    async def add_candidates(candidate_data: AddCandidates):
        await add_record_db(model=candidate_data, orm_table_class=CandidatesDB, foreign_orm_table_class=SkillsDB)

    @staticmethod
    @router.put("/{candidate_id}", status_code=204)
    async def update_candidates(candidate_id: int, data: Candidates):
        invalid_id(id_number=candidate_id)
        await update_record_db(record_id_db=candidate_id, values=data.dict(), orm_table_class=CandidatesDB)

    @staticmethod
    @router.patch("/{candidate_id}")
    async def partial_update_candidates(candidate_id: int, data: PATCHCandidates) -> GetCandidates:
        invalid_id(id_number=candidate_id)
        await update_record_db(record_id_db=candidate_id, values=data.dict(exclude_none=True), orm_table_class=CandidatesDB)
        return (await get_records_db(orm_table_class=CandidatesDB, record_id_db=candidate_id))[0]

    @staticmethod
    @router.delete("/{candidate_id}", status_code=204)
    async def delete_candidates(candidate_id: int):
        invalid_id(id_number=candidate_id)
        await delete_record_db(record_id_db=candidate_id, orm_table_class=CandidatesDB)


class RUDCandidatesSkills:
    router = APIRouter(prefix="/candidates/skills", tags=["RUD candidates skills"])

    @staticmethod
    @router.get("/{skill_id}")
    async def get_skills(skill_id: int) -> GetSkills:
        invalid_id(id_number=skill_id)
        return (await get_records_db(orm_table_class=SkillsDB, record_id_db=skill_id))[0]

    @staticmethod
    @router.put("/{skill_id}", status_code=204)
    async def update_skills(skill_id: int, data: Skills):
        invalid_id(id_number=skill_id)
        await update_record_db(record_id_db=skill_id, values=data.dict(exclude_none=True), orm_table_class=SkillsDB)

    @staticmethod
    @router.patch("/{skill_id}")
    async def partial_update_skills(skill_id: int, data: PATCHSkills) -> GetSkills:
        invalid_id(id_number=skill_id)
        await update_record_db(record_id_db=skill_id, values=data.dict(exclude_none=True), orm_table_class=SkillsDB)
        return (await get_records_db(orm_table_class=SkillsDB, record_id_db=skill_id))[0]

    @staticmethod
    @router.delete("/{skill_id}", status_code=204)
    async def delete_skills(skill_id: int):
        invalid_id(id_number=skill_id)
        await delete_record_db(record_id_db=skill_id, orm_table_class=SkillsDB)


class CRCandidatesSkills:
    router = APIRouter(prefix="/candidates/{candidate_id}/skills", tags=["CR skills of a certain candidate"])

    @staticmethod
    @router.get("")
    async def get_skills(candidate_id: int) -> List[GetCandidatesSkills]:
        invalid_id(id_number=candidate_id)
        return await get_records_db(orm_table_class=SkillsDB, foreign_key=candidate_id)

    @staticmethod
    @router.post("", status_code=201)
    async def add_skills(candidate_id: int, skill_data: Skills):
        await add_record_db(model=skill_data, orm_table_class=SkillsDB, foreign_key=candidate_id)


class CRUDJobOpenings:
    router = APIRouter(prefix="/job-openings", tags=["CRUD job openings"])

    @staticmethod
    @router.get("/{job_openings_id}")
    async def get_job_openings(job_openings_id: int) -> GetJobOpenings:
        invalid_id(id_number=job_openings_id)
        return (await get_records_db(orm_table_class=JobOpeningsDB, record_id_db=job_openings_id))[0]

    @staticmethod
    @router.post("", status_code=201)
    async def add_job_openings(candidate_data: AddJobOpenings):
        await add_record_db(model=candidate_data, orm_table_class=JobOpeningsDB, foreign_orm_table_class=RequiredSkillsDB)

    @staticmethod
    @router.put("/{job_openings_id}", status_code=204)
    async def update_job_openings(job_openings_id: int, data: JobOpenings):
        invalid_id(id_number=job_openings_id)
        await update_record_db(record_id_db=job_openings_id, values=data.dict(), orm_table_class=JobOpeningsDB)

    @staticmethod
    @router.patch("/{job_openings_id}")
    async def partial_update_job_openings(job_openings_id: int, data: PATCHJobOpenings) -> GetJobOpenings:
        invalid_id(id_number=job_openings_id)
        await update_record_db(record_id_db=job_openings_id, values=data.dict(exclude_none=True), orm_table_class=JobOpeningsDB)
        return (await get_records_db(orm_table_class=JobOpeningsDB, record_id_db=job_openings_id))[0]

    @staticmethod
    @router.delete("/{job_openings_id}", status_code=204)
    async def delete_job_openings(job_openings_id: int):
        invalid_id(id_number=job_openings_id)
        await delete_record_db(record_id_db=job_openings_id, orm_table_class=JobOpeningsDB)


class RUDJobOpeningsSkills:
    router = APIRouter(prefix="/job-openings/skills", tags=["RUD job openings skills"])

    @staticmethod
    @router.get("/{skill_id}")
    async def get_skills(skill_id: int) -> GetRequiredSkills:
        invalid_id(id_number=skill_id)
        return (await get_records_db(orm_table_class=RequiredSkillsDB, record_id_db=skill_id))[0]

    @staticmethod
    @router.put("/{skill_id}", status_code=204)
    async def update_skills(skill_id: int, data: RequiredSkills):
        invalid_id(id_number=skill_id)
        await update_record_db(record_id_db=skill_id, values=data.dict(exclude_none=True), orm_table_class=RequiredSkillsDB)

    @staticmethod
    @router.patch("/{skill_id}")
    async def partial_update_skills(skill_id: int, data: PATCHRequiredSkills) -> GetRequiredSkills:
        invalid_id(id_number=skill_id)
        await update_record_db(record_id_db=skill_id, values=data.dict(exclude_none=True), orm_table_class=RequiredSkillsDB)
        return (await get_records_db(orm_table_class=RequiredSkillsDB, record_id_db=skill_id))[0]

    @staticmethod
    @router.delete("/{skill_id}", status_code=204)
    async def delete_skills(skill_id: int):
        invalid_id(id_number=skill_id)
        await delete_record_db(record_id_db=skill_id, orm_table_class=RequiredSkillsDB)


class CRJobOpeningsSkills:
    router = APIRouter(prefix="/job-openings/{skill_id}/skills", tags=["CR skills of a certain job opening"])

    @staticmethod
    @router.get("")
    async def get_skills(skill_id: int) -> List[GetJobOpeningsRequiredSkills]:
        invalid_id(id_number=skill_id)
        return await get_records_db(orm_table_class=RequiredSkillsDB, foreign_key=skill_id)

    @staticmethod
    @router.post("", status_code=201)
    async def add_skills(skill_id: int, skill_data: RequiredSkills):
        await add_record_db(model=skill_data, orm_table_class=RequiredSkillsDB, foreign_key=skill_id)
