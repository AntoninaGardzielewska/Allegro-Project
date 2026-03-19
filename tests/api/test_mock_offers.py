import pytest
from fastapi.testclient import TestClient

from allegro_project.api.mock_offers import get_repository
from allegro_project.main import app
from allegro_project.repositories.offer_repository import OfferRepository
from pydantic import ValidationError

client = TestClient(app)

valid_dictionary = {
    1: {"id": 1, "name": "Test 1", "price": 10.96},
    2: {"id": 2, "name": "Test 1", "price": 12.06},
    3: {"id": 3, "name": "Test 3", "description": "description", "price": 10.96},
    4: {"id": 4, "name": "Test 4", "description": "some text!", "price": 4.28},
}

valid_dictionary_result = [
    {"id": 1, "name": "Test 1", "description": None, "price": 10.96},
    {"id": 2, "name": "Test 1", "description": None, "price": 12.06},
    {"id": 3, "name": "Test 3", "description": "description", "price": 10.96},
    {"id": 4, "name": "Test 4", "description": "some text!", "price": 4.28},
]

empty_dictionary: dict = {}


@pytest.fixture
def override_repository():
    def _override(data):
        def inner():
            return OfferRepository(data)

        app.dependency_overrides[get_repository] = inner

    yield _override
    app.dependency_overrides = {}


def test_get_all_offers(override_repository):
    override_repository(valid_dictionary)
    response = client.get("/offers")
    result = response.json()

    assert response.status_code == 200
    assert result == valid_dictionary_result


def test_get_all_offers_empty_database(override_repository):
    override_repository(empty_dictionary)
    response = client.get("/offers")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "dictionary",
    [
        {1: {"id": "string", "name": "Test", "description": "invalid", "price": 1.0}},
        {1: {"id": 1, "name": "Test", "description": "invalid", "price": -1.0}},
        {1: {"id": 1, "name": "Test", "description": "invalid", "price": -1.0090}},
        {1: {"id": 1, "price": -1.0}},
        {1: {"name": "Test", "description": "invalid", "price": -1.0090}},
        {1: {"id": 1, "name": "Test", "description": "invalid"}},
    ],
)
def test_get_all_offers_invalid_database(override_repository, dictionary):
    override_repository(dictionary)
    with pytest.raises(ValidationError):
        response = client.get("/offers")

        assert response.status_code == 422


@pytest.mark.parametrize("id", [1, 2, 3])
def test_get_offer_by_id(override_repository, id):
    override_repository(valid_dictionary)
    response = client.get(f"/offers/{id}")

    assert response.status_code == 200
    assert response.json() == valid_dictionary_result[id - 1]


@pytest.mark.parametrize("id", [-1, 1, 10, 100])
def test_get_offer_by_id_empty_database(override_repository, id):
    override_repository(empty_dictionary)

    response = client.get(f"/offers/{id}")
    assert response.status_code == 404
    assert response.json()["detail"] is not None


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Test 1", {"id": 1, "name": "Test 1", "description": None, "price": 10.96}),
        ("TEST 1", {"id": 1, "name": "Test 1", "description": None, "price": 10.96}),
        ("test 1", {"id": 1, "name": "Test 1", "description": None, "price": 10.96}),
        (
            "Test 3",
            {"id": 3, "name": "Test 3", "description": "description", "price": 10.96},
        ),
        (
            "4",
            {"id": 4, "name": "Test 4", "description": "some text!", "price": 4.28},
        ),
        (
            "tesT",
            {"id": 4, "name": "Test 4", "description": "some text!", "price": 4.28},
        ),
    ],
)
def test_get_offer_by_name(override_repository, name, expected):
    override_repository(valid_dictionary)
    response = client.get("/best_price/", params={"offer_name": name})

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize("name", ["Test", "Offer", "None"])
def test_get_offer_by_name_empty_database(override_repository, name):
    override_repository(empty_dictionary)
    response = client.get("/best_price/", params={"offer_name": name})

    assert response.status_code == 404
    assert response.json()["detail"] is not None
