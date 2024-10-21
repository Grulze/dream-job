from pydantic import BaseModel, Field, create_model
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


class Pagination(BaseModel):
    limit: int = Field(gt=0, default=10)
    page: int = Field(ge=0, default=0)


class Skills(BaseModel):
    skill_name: str = Field(min_length=3, max_length=30)
    level: int = Field(ge=0, le=2)
    years_of_experience: int = Field(gt=0)
    last_used_year: int = Field(gt=1950, le=2024)


@partial_model
class PATCHSkills(Skills):
    pass


class GetCandidatesSkills(Skills):
    id: int


class GetSkills(Skills):
    foreign_key: int


class Candidates(BaseModel):
    first_name: str = Field(min_length=3, max_length=20)
    second_name: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=16, le=100)
    status: int = Field(ge=0, le=4)
    desired_position: str = Field(min_length=4, max_length=30)
    education_degree: int = Field(ge=0, le=8)
    working_experience: str = Field(max_length=1000)
    about_oneself: str = Field(max_length=1000)
    published: bool


@partial_model
class PATCHCandidates(Candidates):
    pass


class AddCandidates(Candidates):
    skills: List[Skills] | None = None


class GetCandidates(AddCandidates):
    time_create: datetime
    skills: List[GetCandidatesSkills] | None = None
    id: int


class RequiredSkills(BaseModel):
    skill_name: str = Field(min_length=3, max_length=30)
    minimal_level: int
    minimal_years_of_experience: int = Field(gt=0)


@partial_model
class PATCHRequiredSkills(RequiredSkills):
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
    skills: List[RequiredSkills] | None = None


class GetJobOpenings(AddJobOpenings):
    time_create: datetime
    skills: List[GetJobOpeningsRequiredSkills] | None = None
    id: int
