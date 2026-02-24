from fastapi.testclient import TestClient
from requests import Response
from typing import cast

from src.routes.health import app

client = TestClient(app)


def test_health_check():
    response = cast(Response, client.get("/health"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Service is running"}
