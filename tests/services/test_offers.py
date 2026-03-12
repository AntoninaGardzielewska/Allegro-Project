import pytest

from allegro_project.data.mock_offers import database
from allegro_project.models.offer import Offer
from allegro_project.services import mock_offer_service as mock_service
from allegro_project.utils.result import OfferNotFoundError


def test_get_offers_returns_list():
    result = mock_service.get_offers()

    assert isinstance(result, list)
    assert len(result) == len(database)


def test_get_offers_returns_offer_objects():
    result = mock_service.get_offers()
    assert all(isinstance(obj, Offer) for obj in result)


def test_get_offer_by_id_existing():
    result = mock_service.get_offer_by_id(1)

    assert isinstance(result, Offer)
    assert result.id == 1
    assert result.name == "Offer 1"
    assert result.description == "This is first offer"


def test_get_offer_by_id_existing_missing_description():
    result = mock_service.get_offer_by_id(2)

    assert isinstance(result, Offer)
    assert result.description is None


def test_get_offer_by_id_missing():
    with pytest.raises(OfferNotFoundError):
        mock_service.get_offer_by_id(100)
