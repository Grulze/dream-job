from pydantic import BaseModel, Field

from datetime import datetime
from typing import List

from .utils import partial_model
from .candidate_skills import AddCandidateSkills, GetAllCandidateSkills


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
