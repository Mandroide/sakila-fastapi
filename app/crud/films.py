from fastapi import status, HTTPException

from sqlmodel import select, Session, func

from app.models.film import FilmEntity
from app.schemas.films import FilmPublicEntity, FilmFindAllResponse, FilmCreateEntity, FilmFindByIdResponse, \
    FilmUpdateEntity, FilmRemoveResponse

FILM_NOT_FOUND_MESSAGE = "Film not found"


def get_films(page_size: int, page: int, session: Session) -> FilmFindAllResponse:
    total_elements = session.execute(select(func.count(FilmEntity.film_id))).scalar_one()
    total_pages = total_elements // page_size + (1 if total_elements % page_size > 0 else 0)
    offset = page * page_size
    films = session.exec(select(FilmEntity).limit(page_size).offset(offset)).all()
    films = list(map(lambda entity: FilmPublicEntity(**entity.model_dump(exclude={'special_features'}),
                                                     special_features=entity.special_features.split(",")), films))
    return FilmFindAllResponse(page=page, total_elements=total_elements, total_pages=total_pages, content=films)


def create_film(film: FilmCreateEntity, session: Session) -> FilmFindByIdResponse:
    entity = FilmEntity.model_validate(film)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return FilmFindByIdResponse(film=FilmPublicEntity(**entity.model_dump(exclude={'special_features'}),
                                                      special_features=entity.special_features.split(",")))


def get_film(film_id: int, session: Session) -> FilmFindByIdResponse:
    entity = session.get(FilmEntity, film_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)
    return FilmFindByIdResponse(film=FilmPublicEntity(**entity.model_dump(exclude={'special_features'}),
                                                      special_features=entity.special_features.split(",")))


def update_film(session: Session, film_id: int, film: FilmUpdateEntity) -> FilmFindByIdResponse:
    entity = session.get(FilmEntity, film_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)
    data = film.model_dump(exclude_unset=True)
    entity.sqlmodel_update(data)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return FilmFindByIdResponse(film=FilmPublicEntity(**entity.model_dump(exclude={'special_features'}),
                                                      special_features=entity.special_features.split(",")))


def delete_film(session: Session, film_id: int) -> FilmRemoveResponse:
    film = session.get(FilmEntity, film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=FILM_NOT_FOUND_MESSAGE)
    session.delete(film)
    session.commit()
    return FilmRemoveResponse(message="Film deleted")


def get_film_in_stock(film_id: int, in_stock: bool):
    """
    Query the count of films in stock or not in stock
    :param film_id: The film id
    :param in_stock: The in stock flag
    :return:
    """
    return {"film_id": film_id, "actors": [{"actor_id": 1, "first_name": "John", "last_name": "Doe"}]}
