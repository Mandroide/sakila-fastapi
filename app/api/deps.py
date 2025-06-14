from typing import Annotated

from fastapi import Header, HTTPException
from pydantic import BaseModel


class CommonHeaders(BaseModel):
    x_token: str
    authorization: str


async def get_token_header(x_token: Annotated[str, Header()]) -> None:
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str) -> None:
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
