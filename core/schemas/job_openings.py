from pydantic import BaseModel, Field, model_validator

from datetime import datetime
from typing import List

from .utils import partial_model
from .required_skills import AddRequiredSkills, GetJobOpeningsRequiredSkills


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
