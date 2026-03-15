import pytest

from allegro_project.models.offer import Offer
from allegro_project.services import mock_offer_service as service
from allegro_project.utils.result import OfferNotFoundError


@pytest.fixture(scope="session")
def faker_seed(faker):
    faker.seed_instance(42)


class FakeRepository:
    def __init__(self, data):
        self.data = data

    def get_all(self) -> list[Offer]:
        return [Offer.model_validate(offer) for offer in self.data.values()]

    def get_by_id(self, offer_id: int) -> Offer | None:
        offer = self.data.get(offer_id)
        if offer is None:
            return None
        return Offer.model_validate(offer)

    def get_all_by_name(self, offer_name: str) -> list[Offer]:
        result = []
        for offer in self.data.values():
            if offer_name.lower() in offer["name"].lower():
                result.append(Offer.model_validate(offer))
        return result


@pytest.fixture()
def fake_data(request, faker):

    number_of_offers = getattr(request, "param", 0)

    if not isinstance(number_of_offers, int):
        raise TypeError
    if number_of_offers < 0:
        raise ValueError

    db = {}
    for id in range(1, number_of_offers + 1):
        if id % 2:
            description = None
        else:
            description = faker.text(max_nb_chars=20)
        offer = {
            "id": id,
            "name": f"Offer {id}",
            "description": description,
            "price": 1.0,
        }
        db[id] = offer
    return db


@pytest.mark.parametrize(
    "fake_data",
    [
        pytest.param(0, id="empty list"),
        pytest.param(1, id="list with 1 offer"),
        pytest.param(5, id="list with 5 offers"),
    ],
    indirect=True,
)
@pytest.mark.anyio
async def test_get_offers_returns_list_of_offers(fake_data):
    repository = FakeRepository(fake_data)
    result = await service.get_offers(repository)

    assert isinstance(result, list)
    assert len(result) == len(fake_data)
    assert all(isinstance(obj, Offer) for obj in result)


@pytest.mark.parametrize(
    "fake_data",
    [
        pytest.param(1, id="list with 1 offer"),
        pytest.param(5, id="list with 5 offers"),
    ],
    indirect=True,
)
@pytest.mark.anyio
async def test_get_offer_by_id_existing(fake_data):
    repository = FakeRepository(fake_data)

    for key, value in fake_data.items():
        expected = value
        calculated = await service.get_offer_by_id(key, repository)
        calculated_dict = calculated.model_dump()

        assert isinstance(calculated, Offer)
        assert calculated_dict == expected


@pytest.mark.anyio
async def test_get_offer_by_id_empty_database():
    data = {}
    repository = FakeRepository(data)
    with pytest.raises(OfferNotFoundError):
        await service.get_offer_by_id(1, repository)
    with pytest.raises(OfferNotFoundError):
        await service.get_offer_by_id(100, repository)
    with pytest.raises(OfferNotFoundError):
        await service.get_offer_by_id(-1, repository)


@pytest.mark.parametrize(
    "fake_data",
    [
        pytest.param(1, id="list with 1 offer"),
        pytest.param(5, id="list with 5 offers"),
    ],
    indirect=True,
)
@pytest.mark.anyio
async def test_get_offer_by_id_missing_id(fake_data):
    repository = FakeRepository(fake_data)
    with pytest.raises(OfferNotFoundError):
        await service.get_offer_by_id(100, repository)
    with pytest.raises(OfferNotFoundError):
        await service.get_offer_by_id(1000, repository)
    with pytest.raises(OfferNotFoundError):
        await service.get_offer_by_id(-1, repository)
