import datetime
import uuid

from pydantic import BaseModel


class DefaultAPIResponse(BaseModel):
    status_code: int
    message: str
    tid: uuid.UUID | None = None
    owner: str | None = None
    date: datetime.datetime = datetime.datetime.now()

class NotFoundError(Exception):
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name
