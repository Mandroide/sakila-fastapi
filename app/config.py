from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "sakila"
    app_version: str = "0.0.1"
    app_description: str = "sakila api"
    model_config = SettingsConfigDict(extra="allow", env_file=".env")
