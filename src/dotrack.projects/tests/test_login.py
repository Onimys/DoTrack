from fastapi.testclient import TestClient

from src.core.settings import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": "admin@mail.ru",
        "password": "admin",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": "admin@mail.ru",
        "password": "incorrect",
    }
    response = client.post(f"{settings.API_V1_STR}/auth/token", data=login_data)
    assert response.status_code == 400


def test_use_token(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/auth/token/test",
        headers=superuser_token_headers,
    )
    result = response.json()

    assert response.status_code == 200
    assert "email" in result
