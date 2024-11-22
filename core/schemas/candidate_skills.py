from pydantic import BaseModel, Field, model_validator
from .utils import count_score, partial_model


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
    