from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session

from app.core.config import Settings

settings = Settings()
db_url = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_engine(db_url, echo=True)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
