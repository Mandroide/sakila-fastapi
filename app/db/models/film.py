from datetime import datetime

from sqlmodel import Column, Enum, Field, SQLModel

from app.enums.films import Rating


# Todo 2025-05-24 Reemplaza por enums
class FilmBaseEntity(SQLModel):
    title: str = Field(regex="^[A-Za-z ]{1,128}$")
    description: str | None = None
    release_year: int | None = Field(default=None, ge=1900)
    language_id: int = Field(foreign_key="language.language_id", ge=1)
    original_language_id: int | None = Field(
        default=None, foreign_key="language.language_id", ge=1
    )
    rental_duration: int | None = Field(default=None, ge=0)
    rental_rate: float | None = Field(default=None, ge=0)
    length: int | None = Field(default=None, ge=0)
    replacement_cost: float | None = Field(default=None, ge=0)
    rating: Rating | None = Field(
        default=None,
        sa_column=Column(
            name="rating", type_=Enum(Rating, values_callable=Rating.values)
        ),
    )


class FilmEntity(FilmBaseEntity, table=True):
    __tablename__ = "film"
    film_id: int = Field(primary_key=True)
    last_update: datetime | None = None
    special_features: str | None = None
