from fastapi import HTTPException, status
from sqlmodel import Session, func, select

from app.api.v1.schemas.films import (
    FilmCreateEntity,
    FilmFindAllResponse,
    FilmFindByIdResponse,
    FilmPublicEntity,
    FilmRemoveResponse,
    FilmUpdateEntity,
)
from app.db.models.film import FilmEntity

FILM_NOT_FOUND_MESSAGE = "Film not found"


def get_films(page_size: int, page: int, session: Session) -> FilmFindAllResponse:
    result = session.exec(select(func.count(FilmEntity.film_id)))
    total_elements = result.one_or_none() or 0

    total_pages = (total_elements + page_size - 1) // page_size
    offset = page * page_size
    films = session.exec(select(FilmEntity).limit(page_size).offset(offset)).all()
    films_list = [
        FilmPublicEntity(
            **f.model_dump(exclude={"special_features"}),
            special_features=f.special_features.split(","),
        )
        for f in films
    ]
    return FilmFindAllResponse(
        page=page,
        total_elements=total_elements,
        total_pages=total_pages,
        content=films_list,
    )


def create_film(film: FilmCreateEntity, session: Session) -> FilmFindByIdResponse:
    entity = FilmEntity.model_validate(film)
    session.add(entity)
    session.commit()
    session.refresh(entity)

    return FilmFindByIdResponse(
        film=FilmPublicEntity(
            **entity.model_dump(exclude={"special_features"}),
            special_features=(
                entity.special_features.split(",")
                if entity.special_features is not None
                else []
            ),
        )
    )


def get_film(film_id: int, session: Session) -> FilmFindByIdResponse:
    entity = session.get(FilmEntity, film_id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE
        )
    return FilmFindByIdResponse(
        film=FilmPublicEntity(
            **entity.model_dump(exclude={"special_features"}),
            special_features=(
                entity.special_features.split(",")
                if entity.special_features is not None
                else []
            ),
        )
    )


def update_film(
    session: Session, film_id: int, film: FilmUpdateEntity
) -> FilmFindByIdResponse:
    entity = session.get(FilmEntity, film_id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE
        )
    data = film.model_dump(exclude_unset=True)
    entity.sqlmodel_update(data)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return FilmFindByIdResponse(
        film=FilmPublicEntity(
            **entity.model_dump(exclude={"special_features"}),
            special_features=(
                entity.special_features.split(",")
                if entity.special_features is not None
                else []
            ),
        )
    )


def delete_film(session: Session, film_id: int) -> FilmRemoveResponse:
    film = session.get(FilmEntity, film_id)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE
        )
    session.delete(film)
    session.commit()
    return FilmRemoveResponse(message="Film deleted")


def get_film_in_stock(film_id: int, in_stock: bool) -> dict[str, object]:
    """
    Query the count of films in stock or not in stock
    :param film_id: The film id
    :param in_stock: The in stock flag
    :return:
    """
    return {
        "film_id": film_id,
        "actors": [{"actor_id": 1, "first_name": "John", "last_name": "Doe"}],
    }
