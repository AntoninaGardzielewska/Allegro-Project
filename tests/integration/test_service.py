from allegro_project.models.offer import Offer
from allegro_project.services import mock_offer_service as service
from allegro_project.api.mock_offers import get_repository
import pytest


@pytest.mark.anyio
async def test_get_offers_default_repository():
    repository = get_repository()
    result = await service.get_offers(repository)

    assert isinstance(result, list)
    assert all(isinstance(obj, Offer) for obj in result)
