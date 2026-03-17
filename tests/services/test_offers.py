from unittest.mock import Mock

import pytest

from allegro_project.models.offer import Offer
from allegro_project.services import mock_offer_service as service
from allegro_project.utils.result import OfferNotFoundError


@pytest.fixture(scope="session")
def faker_seed(faker):
    faker.seed_instance(42)


@pytest.fixture()
def fake_data(request, faker):

    number_of_offers = getattr(request, "param", 0)

    result = []
    for i in range(1, number_of_offers + 1):
        description = None if i % 2 else faker.text(max_nb_chars=20)
        result.append(
            Offer(
                id=i,
                name=f"Offer {i}",
                description=description,
                price=float(i),
            )
        )

    return result


@pytest.mark.parametrize(
    "fake_data",
    [
        pytest.param(0, id="empty list"),
        pytest.param(1, id="single offer"),
        pytest.param(5, id="multiple offers"),
    ],
    indirect=True,
)
@pytest.mark.anyio
async def test_get_offers_returns_list_of_offers(fake_data):
    repository = Mock()
    repository.get_all.return_value = fake_data

    result = await service.get_offers(repository)

    assert isinstance(result, list)
    assert len(result) == len(fake_data)
    assert all(isinstance(obj, Offer) for obj in result)
    assert result == fake_data

    repository.get_all.assert_called_once_with()


@pytest.mark.parametrize(
    "fake_data, offer_id",
    [
        pytest.param(1, 1, id="single offer"),
        pytest.param(5, 1, id="multiple offers check id 1"),
        pytest.param(5, 5, id="multiple offers check id 5"),
        pytest.param(50, 50, id="multiple offers check id 50"),
    ],
    indirect=["fake_data"],
)
@pytest.mark.anyio
async def test_get_offer_by_id_existing(fake_data, offer_id):
    repository = Mock()
    repository.get_by_id.side_effect = lambda x: (
        fake_data[x - 1] if 1 <= x <= len(fake_data) else None
    )

    expected = fake_data[offer_id - 1]

    calculated = await service.get_offer_by_id(offer_id, repository)

    assert isinstance(calculated, Offer)
    assert calculated == expected

    repository.get_by_id.assert_called_once_with(offer_id)


@pytest.mark.parametrize(
    "fake_data, offer_id",
    [
        pytest.param(0, 1, id="empty list"),
        pytest.param(1, 10, id="single offer"),
        pytest.param(5, 10, id="multiple offers"),
        pytest.param(5, -1, id="multiple offers negative id"),
        pytest.param(5, 0, id="multiple offers id=0"),
    ],
    indirect=["fake_data"],
)
@pytest.mark.anyio
async def test_get_offer_by_missing_id(fake_data, offer_id):
    repository = Mock()
    repository.get_by_id.side_effect = lambda x: (
        fake_data[x - 1] if 1 <= x <= len(fake_data) else None
    )

    with pytest.raises(OfferNotFoundError):
        await service.get_offer_by_id(offer_id, repository)

    repository.get_by_id.assert_called_once_with(offer_id)
