from fastapi.testclient import TestClient

from allegro_project.main import app

client = TestClient(app)


def test_get_offers_happy_path():
    response = client.get("/offers")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]

    assert "id" in first
    assert "name" in first
    assert "description" in first


def test_get_offer_by_id_happy_path():
    response = client.get("/offers/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Offer 1"
