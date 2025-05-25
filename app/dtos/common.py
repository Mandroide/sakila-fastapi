from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    page_size: int = Field(default=10, ge=1, le=100)
    page: int = Field(default=0, ge=0)
    sort: Literal["id", "last_update"] = "id"
    order: str = Field(default="asc", min_length=1)

class Tags(Enum):
    countries = "countries"
    films = "films"
    customers = "customers"
    staff = "staff"
    languages = "languages"
    categories = "categories"
    actors = "actors"