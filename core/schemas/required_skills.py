from pydantic import BaseModel, Field, model_validator
from .utils import count_score, partial_model


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
