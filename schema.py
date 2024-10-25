from enum import Enum

from pydantic import BaseModel, Field, create_model, model_validator
from pydantic.fields import FieldInfo

from copy import deepcopy
from datetime import datetime
from typing import List, Optional, Type, Any, Tuple


def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        }
    )


def count_score(level, year):
    return (level + 1) * 1000 + year * 400


class EnumSorting(Enum):
    from_the_lower = 'lower'
    from_the_upper = 'upper'


class Sorting(BaseModel):
    sorting_from: EnumSorting = EnumSorting.from_the_lower


class Pagination(BaseModel):
    limit: int = Field(gt=0, default=10)
    page: int = Field(ge=0, default=0)


class CandidateSkills(BaseModel):
    skill_name: str = Field(min_length=1, max_length=30)
    level: int = Field(ge=0, le=2)
    years_of_experience: int = Field(gt=0)
    last_used_year: int = Field(gt=1950, le=2024)


class AddCandidateSkills(CandidateSkills):
    indexing_skill_name: str | None = None
    score: int | None = None

    @model_validator(mode='after')
    def index_name(self):
        if self.skill_name:
            self.indexing_skill_name = self.skill_name.lower()
        else:
            self.indexing_skill_name = None
        return self

    @model_validator(mode='after')
    def get_score(self):
        this_year = 2024
        if not (self.level is None) and self.years_of_experience:
            self.score = count_score(level=self.level, year=self.years_of_experience)
            if self.last_used_year:
                self.score = self.score - min(((this_year - self.last_used_year) ** 2) * 30, int(self.score / 3))
        else:
            self.score = None
        return self


@partial_model
class PATCHCandidateSkills(AddCandidateSkills):
    pass


class GetAllCandidateSkills(CandidateSkills):
    id: int


class GetCandidateSkills(CandidateSkills):
    foreign_key: int


class Candidates(BaseModel):
    first_name: str = Field(min_length=3, max_length=20)
    second_name: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=16, le=100)
    status: int = Field(ge=0, le=4)
    city: str = Field(min_length=3, max_length=20)
    desired_position: str = Field(min_length=4, max_length=30)
    education_degree: int = Field(ge=0, le=8)
    working_experience: str = Field(max_length=1000)
    about_oneself: str = Field(max_length=1000)
    published: bool


@partial_model
class PATCHCandidates(Candidates):
    pass


class AddCandidates(Candidates):
    skills: List[AddCandidateSkills] | None = None


class GetCandidates(AddCandidates):
    time_create: datetime
    skills: List[GetAllCandidateSkills] | None = None
    id: int


class RequiredSkills(BaseModel):
    skill_name: str = Field(min_length=1, max_length=30)
    level: int
    years_of_experience: int = Field(gt=0)


class AddRequiredSkills(RequiredSkills):
    indexing_skill_name: str | None = None
    score: int | None = None

    @model_validator(mode='after')
    def index_name(self):
        if self.skill_name:
            self.indexing_skill_name = self.skill_name.lower()
        else:
            self.indexing_skill_name = None
        return self

    @model_validator(mode='after')
    def get_score(self):
        if not (self.level is None) and self.years_of_experience:
            self.score = count_score(level=self.level, year=self.years_of_experience)
        else:
            self.score = None
        return self


@partial_model
class PATCHRequiredSkills(AddRequiredSkills):
    pass


class GetJobOpeningsRequiredSkills(RequiredSkills):
    id: int


class GetRequiredSkills(RequiredSkills):
    foreign_key: int


class JobOpenings(BaseModel):
    title: str = Field(min_length=4, max_length=40)
    description: str = Field(max_length=1000)
    address: str = Field(max_length=100)
    salary: int = Field(gt=0)


@partial_model
class PATCHJobOpenings(JobOpenings):
    pass


class AddJobOpenings(JobOpenings):
    skills: List[AddRequiredSkills] | None = None
    skills_quantity: int | None = None

    @model_validator(mode='after')
    def skills_counting(self):
        if self.skills:
            self.skills_quantity = len(self.skills)
        else:
            self.skills_quantity = 0
        return self


class GetJobOpenings(JobOpenings):
    time_create: datetime
    skills: List[GetJobOpeningsRequiredSkills] | None = None
    id: int
