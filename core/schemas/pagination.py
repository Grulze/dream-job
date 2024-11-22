from enum import Enum
from pydantic import BaseModel, Field


class EnumSorting(Enum):
    from_the_lower = 'lower'
    from_the_upper = 'upper'


class Sorting(BaseModel):
    sorting_from: EnumSorting = EnumSorting.from_the_lower


class Pagination(BaseModel):
    limit: int = Field(gt=0, default=10)
    page: int = Field(ge=0, default=0)
