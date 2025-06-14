from fastapi import status

from tests.conftest import client


def test_get_films() -> None:
    response = client.get("/films")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data is not None
