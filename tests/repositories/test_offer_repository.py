import pytest
from pydantic import ValidationError

from allegro_project.models.offer import Offer
from allegro_project.repositories.offer_repository import OfferRepository

valid_database = {
    1: {"id": 1, "name": "Offer 1", "description": "This is first offer"},
    2: {"id": 2, "name": "Offer 2"},
    3: {
        "id": 3,
        "name": "Offer 3",
        "description": "This is third object",
    },
}


def test_repository_get_all():
    repository = OfferRepository(valid_database)

    result = repository.get_all()

    assert isinstance(result, list)
    assert all(isinstance(obj, Offer) for obj in result)
    assert len(valid_database) == len(result)


def test_repository_get_all_empty_database():
    database = {}
    repository = OfferRepository(database)

    result = repository.get_all()
    assert isinstance(result, list)
    assert result == []


@pytest.mark.parametrize(
    "database",
    [
        pytest.param(
            {
                1: {
                    "id": "number",
                    "name": "Offer 1",
                    "description": "This is first offer",
                }
            },
            id="list with id being a string",
        ),
        pytest.param(
            {
                1: {
                    "id": [1],
                    "name": "Offer 1",
                    "description": "This is first offer",
                }
            },
            id="list with id being list",
        ),
        pytest.param(
            {
                1: {
                    "name": "Offer 1",
                    "description": "This is first offer",
                }
            },
            id="list with missing id",
        ),
        pytest.param(
            {
                1: {
                    "id": 1,
                    "description": "This is first offer",
                }
            },
            id="list with missing name",
        ),
        pytest.param(
            {1: {}},
            id="missing data",
        ),
    ],
)
def test_repository_get_all_incorrect_values_in_database(database):
    repository = OfferRepository(database)
    with pytest.raises(ValidationError):
        repository.get_all()


def test_repository_get_by_id_happy_path():
    repository = OfferRepository(valid_database)

    for key, value in valid_database.items():
        result = repository.get_by_id(key)
        assert isinstance(result, Offer)
        assert result == Offer(**value)


@pytest.mark.parametrize("id", [1, 100, -1])
def test_repository_get_by_id_missing_id(id):
    database = {}
    repository = OfferRepository(database)

    result = repository.get_by_id(id)
    assert result is None


def test_repository_get_by_id_incorrect_data():
    database = {
        1: {"id": "number", "name": "Offer 1", "description": "This is first offer"}
    }
    repository = OfferRepository(database)

    with pytest.raises(ValidationError):
        repository.get_by_id(1)
