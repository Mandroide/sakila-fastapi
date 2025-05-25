from functools import lru_cache
from typing import Annotated, Any, Coroutine

from fastapi import FastAPI, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)

from .config import Settings
from .exceptions import DefaultAPIResponse
# from .dependencies import get_query_token
from .routers import countries, films
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(
    countries.router,
    prefix="/api/v1"
)

app.include_router(
    films.router,
    prefix="/api/v1"
)


@lru_cache
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_description": settings.app_description,
        "db_host": settings.db_host,
        "db_port": settings.db_port,
        "db_name": settings.db_name,
        "db_user": settings.db_user,
        "db_password": settings.db_password,
    }

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=jsonable_encoder(
                            DefaultAPIResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(exc))))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=jsonable_encoder(
                            DefaultAPIResponse(status_code=status.HTTP_400_BAD_REQUEST, message=str(exc))))
