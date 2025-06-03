import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "sakila"
    app_version: str = "0.0.1"
    app_description: str = "sakila api"
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = os.getenv("DB_PORT", 3306)
    db_name: str = os.getenv("DB_NAME", "sakila")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
