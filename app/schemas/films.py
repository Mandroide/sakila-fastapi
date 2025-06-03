from pydantic import BaseModel

from app.models.film import FilmBaseEntity


class FilmPublicEntity(FilmBaseEntity):
    film_id: int
    special_features: set[str] | None = None


class FilmCreateEntity(FilmBaseEntity):
    special_features: set[str] | None = None


class FilmUpdateEntity(FilmBaseEntity):
    special_features: set[str] | None = None


class FilmFindAllResponse(BaseModel):
    page: int
    total_elements: int
    total_pages: int
    content: list[FilmPublicEntity]


class FilmFindByIdResponse(BaseModel):
    film: FilmPublicEntity


class FilmRemoveResponse(BaseModel):
    message: str
