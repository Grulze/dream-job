from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from request_db import add_skills_db, add_model_db, delete_record_db, get_model_db, update_record_db, \
    find_suitable_records, get_skills_db, delete_required_skill_db
from database import CandidatesDB, CandidatesSkillsDB, JobOpeningsDB, RequiredSkillsDB
from schema import GetCandidateSkills, AddCandidates, Candidates, PATCHCandidates, GetCandidates, \
    PATCHCandidateSkills, GetAllCandidateSkills, GetJobOpenings, AddJobOpenings, JobOpenings, PATCHJobOpenings,\
    GetRequiredSkills, PATCHRequiredSkills, GetJobOpeningsRequiredSkills, Pagination, Sorting, AddCandidateSkills, \
    AddRequiredSkills
from custom_exceptions import invalid_id


class SelectionOfCandidatesAndJobOpenings:
    router = APIRouter(prefix="", tags=["Selection of candidates and job openings"])

    @staticmethod
    @router.get("/job-openings/{job_id}/selection", response_model=List[GetCandidates])
    @cache(1, namespace="job_openings_selection")
    async def get_suitable_candidates(job_id: int, pagination: Pagination = Depends(),
                                      sorting_param: Sorting = Depends()) -> List[GetCandidates]:
        """
        Return all suitable candidates from database with pagination.
        :param job_id: id of the job openings being searched for.
        :param pagination: class with information that used for pagination.
        :param sorting_param: parameter by which sorting will be performed, 'lower' - from less qualified,
        'upper' - from more qualified.
        :return: List[GetCandidates]
        """
        invalid_id(job_id)
        return await find_suitable_records(
            record_id=job_id, orm_table_for_search=CandidatesDB, lim=pagination.limit, page=pagination.page,
            sorting=sorting_param.sorting_from.value
        )

    @staticmethod
    @router.get("/candidates/{candidate_id}/selection", response_model=List[GetJobOpenings])
    @cache(1, namespace="candidates_selection")
    async def get_suitable_job_openings(candidate_id: int, pagination: Pagination = Depends(),
                                        sorting_param: Sorting = Depends()) -> List[GetJobOpenings]:
        """
        Return all suitable job openings from database with pagination.
        :param candidate_id: id of the candidates being searched for.
        :param pagination: class with information that used for pagination.
        :param sorting_param: parameter by which sorting will be performed, 'lower' - from less qualified,
        'upper' - from more qualified.
        :return: List[GetJobOpenings]
        """
        invalid_id(candidate_id)
        return await find_suitable_records(
            record_id=candidate_id, orm_table_for_search=JobOpeningsDB, lim=pagination.limit, page=pagination.page,
            sorting=sorting_param.sorting_from.value
        )


class AllCandidatesAndJobOpenings:
    router = APIRouter(tags=["Get all candidates and job openings"])

    @staticmethod
    @router.get("/candidates", response_model=List[GetCandidates])
    @cache(1, namespace="all_candidates_with_pagination")
    async def get_all_candidates(pagination: Pagination = Depends()) -> List[GetCandidates]:
        """
        Return all candidates from database with pagination.
        :param pagination: class with information that used for pagination
        :return: List[GetCandidates]
        """

        return await get_model_db(orm_table_class=CandidatesDB, lim=pagination.limit, page=pagination.page)

    @staticmethod
    @router.get("/job-openings", response_model=List[GetJobOpenings])
    @cache(1, namespace="all_job_openings_with_pagination")
    async def get_job_openings(pagination: Pagination = Depends()) -> List[GetJobOpenings]:
        """
        Return all job openings from database with pagination.
        :param pagination: class with information that used for pagination.
        :return: List[GetCandidates]
        """
        return await get_model_db(orm_table_class=JobOpeningsDB, lim=pagination.limit, page=pagination.page)


class CRUDCandidates:
    router = APIRouter(prefix="/candidates", tags=["CRUD candidates"])

    @staticmethod
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

    @staticmethod
    @router.post("", status_code=201)
    async def add_candidates(candidate_data: AddCandidates):
        """
        Creating new candidate.
        :param candidate_data: data about candidate.
        """
        await add_model_db(
            model=candidate_data, orm_table_class=CandidatesDB, foreign_orm_table_class=CandidatesSkillsDB
        )

    @staticmethod
    @router.put("/{candidate_id}", status_code=204)
    async def update_candidates(candidate_id: int, data: Candidates):
        """
        Full update data about candidate.
        :param candidate_id: id of candidate in table.
        :param data: new data about candidate.
        """
        invalid_id(id_number=candidate_id)
        await update_record_db(record_id_db=candidate_id, values=data.dict(), orm_table_class=CandidatesDB)

    @staticmethod
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

    @staticmethod
    @router.delete("/{candidate_id}", status_code=204)
    async def delete_candidates(candidate_id: int):
        """
        Delete candidate from table in database.
        :param candidate_id: id of candidate in table.
        """
        invalid_id(id_number=candidate_id)
        await delete_record_db(record_id_db=candidate_id, orm_table_class=CandidatesDB)


class RUDCandidatesSkills:
    router = APIRouter(prefix="/candidates/skills", tags=["RUD candidates skills"])

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    @router.delete("/{skill_id}", status_code=204)
    async def delete_skills(skill_id: int):
        """
        Delete skill of candidate from table in database.
        :param skill_id: id of skill in table.
        """
        invalid_id(id_number=skill_id)
        await delete_record_db(record_id_db=skill_id, orm_table_class=CandidatesSkillsDB)


class CRCandidatesSkills:
    router = APIRouter(prefix="/candidates/{candidate_id}/skills", tags=["CR skills of a certain candidate"])

    @staticmethod
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

    @staticmethod
    @router.post("", status_code=201)
    async def add_skills(candidate_id: int, skills_data: List[AddCandidateSkills]):
        """
        Creating new skills of candidate.
        :param candidate_id: id of candidate in table.
        :param skills_data: list with dicts of skills data.
        """
        await add_skills_db(skills=skills_data, orm_table_class=CandidatesSkillsDB, foreign_key=candidate_id)


class CRUDJobOpenings:
    router = APIRouter(prefix="/job-openings", tags=["CRUD job openings"])

    @staticmethod
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

    @staticmethod
    @router.post("", status_code=201)
    async def add_job_openings(candidate_data: AddJobOpenings):
        """
        Creating new job opening.
        :param candidate_data: data about job opening.
        """
        await add_model_db(model=candidate_data, orm_table_class=JobOpeningsDB,
                           foreign_orm_table_class=RequiredSkillsDB)

    @staticmethod
    @router.put("/{job_openings_id}", status_code=204)
    async def update_job_openings(job_openings_id: int, data: JobOpenings):
        """
        Full update data about job opening.
        :param job_openings_id: id of job opening in database.
        :param data: new data about job opening.
        """
        invalid_id(id_number=job_openings_id)
        await update_record_db(record_id_db=job_openings_id, values=data.dict(), orm_table_class=JobOpeningsDB)

    @staticmethod
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

    @staticmethod
    @router.delete("/{job_openings_id}", status_code=204)
    async def delete_job_openings(job_openings_id: int):
        """
        Delete job opening from table in database.
        :param job_openings_id: id of job opening in database.
        """
        invalid_id(id_number=job_openings_id)
        await delete_record_db(record_id_db=job_openings_id, orm_table_class=JobOpeningsDB)


class RUDJobOpeningsSkills:
    router = APIRouter(prefix="/job-openings/skills", tags=["RUD job openings skills"])

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    @router.delete("/{skill_id}", status_code=204)
    async def delete_skills(skill_id: int):
        """
        Delete skill of job opening from table in database.
        :param skill_id: id of skill in table.
        """
        invalid_id(id_number=skill_id)
        await delete_required_skill_db(record_id_db=skill_id)


class CRJobOpeningsSkills:
    router = APIRouter(prefix="/job-openings/{job_openings_id}/skills", tags=["CR skills of a certain job opening"])

    @staticmethod
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

    @staticmethod
    @router.post("", status_code=201)
    async def add_skills(job_openings_id: int, skills_data: List[AddRequiredSkills]):
        """
        Creating new skills of job opening.
        :param job_openings_id: id of job opening in database.
        :param skills_data: list with dicts of skills data.
        """
        await add_skills_db(skills=skills_data, orm_table_class=RequiredSkillsDB, foreign_key=job_openings_id)
