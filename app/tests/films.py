from fastapi import status

from app.tests.conftest import client


def test_get_films():
    response = client.get("/films")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data is not None