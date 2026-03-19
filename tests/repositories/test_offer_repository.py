import pytest
from pydantic import ValidationError

from allegro_project.models.offer import Offer
from allegro_project.repositories.offer_repository import OfferRepository

valid_database = {
    1: {"id": 1, "name": "Offer 1", "description": "This is first offer", "price": 1.2},
    2: {"id": 2, "name": "Offer 2", "price": 3.43},
    3: {
        "id": 3,
        "name": "Offer 3",
        "description": "This is third object",
        "price": 12.32,
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


def test_get_all_mixed_valid_and_invalid():
    database = {
        1: {"id": 1, "name": "Offer 1", "price": 1.2},
        2: {"id": "bad", "name": "Offer 2"},
    }
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


def test_get_all_by_name_found():
    repository = OfferRepository(valid_database)

    result = repository.get_all_by_name("Offer")

    assert len(result) == 3


def test_get_all_by_name_case_insensitive():
    repository = OfferRepository(valid_database)

    result = repository.get_all_by_name("offer 1")

    assert len(result) == 1
    assert result[0].name == "Offer 1"


def test_get_all_by_name_partial_match():
    repository = OfferRepository(valid_database)

    result = repository.get_all_by_name("1")

    assert len(result) == 1


def test_get_all_by_name_not_found():
    repository = OfferRepository(valid_database)

    result = repository.get_all_by_name("XYZ")

    assert result == []


def test_repository_does_not_modify_input():
    import copy

    database = copy.deepcopy(valid_database)

    repository = OfferRepository(database)
    repository.get_all()

    assert database == valid_database
