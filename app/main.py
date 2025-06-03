from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from app.core.config import Settings
from app.utils.exceptions import DefaultAPIResponse

from .api.v1.routers import countries, films

app = FastAPI()
app.include_router(countries.router, prefix="/api/v1")

app.include_router(films.router, prefix="/api/v1")


@lru_cache
def get_settings() -> Settings:
    return Settings()


@app.get("/info")
async def info(
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, object]:
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
async def custom_http_exception_handler(
    request: Request, exc: HTTPException
) -> Response:
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            DefaultAPIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(exc)
            )
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            DefaultAPIResponse(
                status_code=status.HTTP_400_BAD_REQUEST, message=str(exc)
            )
        ),
    )
