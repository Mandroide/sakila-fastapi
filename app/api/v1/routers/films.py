from typing import Annotated

from fastapi import APIRouter, Path, Query, status

import app.db.repositories.films as films_crud
from app.api.v1.schemas.common import FilterParams
from app.api.v1.schemas.films import (
    FilmCreateEntity,
    FilmFindAllResponse,
    FilmFindByIdResponse,
    FilmRemoveResponse,
    FilmUpdateEntity,
)
from app.db.engine import SessionDep
from app.enums.common import Prefix, Tags

FILM_NOT_FOUND_MESSAGE = "Film not found"

router = APIRouter(
    prefix=Prefix.films,
    tags=[Tags.films],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_films(
    session: SessionDep, filter_query: Annotated[FilterParams, Query()]
) -> FilmFindAllResponse:
    page = filter_query.page
    page_size = filter_query.page_size
    return films_crud.get_films(page_size, page, session)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_film(
    film: FilmCreateEntity, session: SessionDep
) -> FilmFindByIdResponse:
    return films_crud.create_film(film, session)


@router.get("/{film_id}")
async def get_film(session: SessionDep, film_id: int) -> FilmFindByIdResponse:
    return films_crud.get_film(film_id, session)


@router.put("/{film_id}")
async def update_film(
    session: SessionDep, film_id: int, film: FilmUpdateEntity
) -> FilmFindByIdResponse:
    return films_crud.update_film(session, film_id, film)


@router.delete("/{film_id}")
async def delete_film(session: SessionDep, film_id: int) -> FilmRemoveResponse:
    return films_crud.delete_film(session, film_id)


@router.get(
    "inventory/{film_id}",
    summary="Get film in stock",
    response_description="The count of films in stock",
)
async def get_film_in_stock(
    film_id: Annotated[int, Path(ge=1)], in_stock: Annotated[bool, Query()] = True
) -> dict[str, object]:
    """
    Query the count of films in stock or not in stock
    :param film_id: The film id
    :param in_stock: The in stock flag
    :return:
    """
    return films_crud.get_film_in_stock(film_id, in_stock)
