from typing import Annotated

from fastapi import APIRouter, Query, Path, status, HTTPException
from sqlalchemy import func
from sqlmodel import select

from app.dtos.common import FilterParams, Tags
from app.engine import SessionDep
from app.entity.film import FilmEntity, FilmCreateEntity, FilmFindByIdResponse, FilmPublicEntity, FilmFindAllResponse, \
    FilmUpdateEntity, FilmRemoveResponse

FILM_NOT_FOUND_MESSAGE = "Film not found"

router = APIRouter(
    prefix="/films",
    tags=[Tags.films],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get_films(session: SessionDep, filter_query: Annotated[FilterParams, Query()]) -> FilmFindAllResponse:
    page = filter_query.page
    page_size = filter_query.page_size
    total_elements = session.execute(select(func.count(FilmEntity.film_id))).scalar_one()
    total_pages = total_elements // page_size + (1 if total_elements % page_size > 0 else 0)
    offset = page * page_size
    films = session.exec(select(FilmEntity).limit(page_size).offset(offset)).all()
    films = list(map(lambda entity: FilmPublicEntity(**entity.model_dump(exclude={'special_features'}), special_features=entity.special_features.split(",")), films))
    return FilmFindAllResponse(page=page, total_elements=total_elements, total_pages=total_pages, content=films)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_film(film: FilmCreateEntity, session: SessionDep) -> FilmFindByIdResponse:
    entity = FilmEntity.model_validate(film)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return FilmFindByIdResponse(film=FilmPublicEntity(**entity.model_dump(exclude={'special_features'}), special_features=entity.special_features.split(",")))


@router.get("/{film_id}")
async def get_film(session: SessionDep, film_id: int) -> FilmFindByIdResponse:
    entity = session.get(FilmEntity, film_id)
    print(entity)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)
    return FilmFindByIdResponse(film=FilmPublicEntity(**entity.model_dump(exclude={'special_features'}), special_features=entity.special_features.split(",")))


@router.put("/{film_id}")
async def update_film(session: SessionDep, film_id: int, film: FilmUpdateEntity) -> FilmFindByIdResponse:
    entity = session.get(FilmEntity, film_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)
    data = film.model_dump(exclude_unset=True)
    entity.sqlmodel_update(data)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return FilmFindByIdResponse(film=FilmPublicEntity(**entity.model_dump(exclude={'special_features'}), special_features=entity.special_features.split(",")))


@router.delete("/{film_id}")
async def delete_film(session: SessionDep, film_id: int) -> FilmRemoveResponse:
    film = session.get(FilmEntity, film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)
    session.delete(film)
    session.commit()
    return FilmRemoveResponse(message="Film deleted")


@router.get(
    "inventory/{film_id}",
    summary="Get film in stock",
    response_description="The count of films in stock",
)
async def get_film_in_stock(film_id: Annotated[int, Path(ge=1)], in_stock: Annotated[bool, Query()] = True):
    """
    Query the count of films in stock or not in stock
    :param film_id: The film id
    :param in_stock: The in stock flag
    :return:
    """
    return {"film_id": film_id, "actors": [{"actor_id": 1, "first_name": "John", "last_name": "Doe"}]}
