from pydantic import BaseModel, Field


class CountryRequest(BaseModel):
    country_id: int
    country: str = Field(pattern="^[A-Za-z ]{1,50}$")


class CountryDto(BaseModel):
    country_id: int
    country: str


class CountryFindAllResponse(BaseModel):
    offset: int
    limit: int
    total_elements: int
    total_pages: int
    content: list[CountryDto]


class CountryFindByIdResponse(BaseModel):
    country: CountryDto


class CountryRemoveResponse(BaseModel):
    message: str
