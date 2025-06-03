from fastapi.testclient import TestClient

from app.core.config import Settings

from ..main import app, get_settings


def get_settings_override() -> Settings:
    return Settings(
        app_name="sakila_test", app_version="0.0.1", app_description="sakila api test"
    )


settings = Settings()
app.dependency_overrides[get_settings] = get_settings_override
client = TestClient(app)
