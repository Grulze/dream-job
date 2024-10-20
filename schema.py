from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo

from copy import deepcopy
from datetime import datetime
from typing import List, Optional, Type, Any, Tuple


def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
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

class CRUDSkills(BaseModel):
    candidate_id: int = Field(gt=0)
    skill_name: str = Field(min_length=3, max_length=30)
    years_of_experience: int = Field(gt=0)
    last_used_year: int = Field(gt=1950, le=2024)


class RelationshipSkills(CRUDSkills):
    skill_id: int


class UpdateCandidates(BaseModel):
    first_name: str = Field(min_length=3, max_length=20)
    second_name: str = Field(min_length=3, max_length=20)
    age: int = Field(gt=16, le=100)
    status: int = Field(ge=0, le=4)
    desired_position: str = Field(min_length=4, max_length=30)
    education_degree: int = Field(ge=0, le=8)
    working_experience: str = Field(max_length=1000)
    about_oneself: str = Field(max_length=1000)
    published: bool


@partial_model
class PATCHCandidates(UpdateCandidates):
    pass
#     first_name: str | None = Field(min_length=3, max_length=20, default=None)
#     second_name: str | None = Field(min_length=3, max_length=20, default=None)
#     age: int | None = Field(gt=16, le=100, default=None)
#     status: int | None = Field(ge=0, le=4, default=None)
#     desired_position: str | None = Field(min_length=4, max_length=30, default=None)
#     education_degree: int | None = Field(ge=0, le=8, default=None)
#     working_experience: str | None = Field(max_length=1000, default=None)
#     about_oneself: str | None = Field(max_length=1000, default=None)
#     published: bool | None = None


class AddCandidates(UpdateCandidates):
    skills: List[CRUDSkills] | None = None


class GetCandidate(AddCandidates):
    time_create: datetime
