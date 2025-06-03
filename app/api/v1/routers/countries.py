from typing import Annotated

from fastapi import APIRouter, Body, Path, Query, status

from app.api.v1.schemas.common import FilterParams
from app.db.models.countries import (
    CountryDto,
    CountryFindAllResponse,
    CountryFindByIdResponse,
    CountryRequest,
)
from app.enums.common import Prefix, Tags

router = APIRouter(
    prefix=Prefix.countries,
    tags=[Tags.countries],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_countries(
    filter_query: Annotated[FilterParams, Query()],
) -> CountryFindAllResponse:
    return CountryFindAllResponse(
        offset=filter_query.page,
        limit=filter_query.page_size,
        total_elements=10,
        total_pages=1,
        content=[
            CountryDto(country_id=1, country="Germany"),
            CountryDto(country_id=2, country="France"),
            CountryDto(country_id=3, country="Spain"),
        ],
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_country(country: CountryRequest) -> CountryFindByIdResponse:
    print(**country.model_dump())
    return CountryFindByIdResponse(
        country=CountryDto(country_id=country.country_id, country=country.country)
    )


@router.get("/{country_id}")
async def get_country(
    country_id: Annotated[int, Path(ge=1)],
) -> CountryFindByIdResponse:
    return CountryFindByIdResponse(
        country=CountryDto(country_id=country_id, country="Germany")
    )


@router.put("/{country_id}")
async def update_country(
    country_id: Annotated[int, Path(ge=1)], country: Annotated[CountryRequest, Body()]
) -> CountryFindByIdResponse:
    return CountryFindByIdResponse(
        country=CountryDto(country_id=country_id, country="Germany")
    )


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(country_id: Annotated[int, Path(ge=1)]) -> None:
    pass
