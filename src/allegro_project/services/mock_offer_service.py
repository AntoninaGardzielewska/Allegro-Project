from allegro_project.models.offer import Offer
from allegro_project.repositories.offer_repository import OfferRepository
from allegro_project.utils.result import OfferNotFoundError


def get_offers(repository=None) -> list[Offer]:
    repository = repository or OfferRepository()
    return repository.get_all()


def get_offer_by_id(offer_id: int, repository=None) -> Offer:
    repository = repository or OfferRepository()
    offer = repository.get_by_id(offer_id)
    if offer is None:
        raise OfferNotFoundError(f"Offer with id {offer_id} not found")
    return offer
