import logging

from allegro_project.interfaces.repository import Repository
from allegro_project.models.offer import Offer
from allegro_project.utils.find_best_offer import find_best_offer_from_list
from allegro_project.utils.result import OfferNotFoundError

logger = logging.getLogger(__name__)


async def get_offers(repository: Repository) -> list[Offer]:
    return repository.get_all()


async def get_offer_by_id(offer_id: int, repository: Repository) -> Offer:
    offer = repository.get_by_id(offer_id)
    if offer is None:
        raise OfferNotFoundError(f"Offer with id {offer_id} not found")
    return offer


async def find_best_offer_by_name(offer_name: str, repository: Repository) -> Offer:
    matching_offers = repository.get_all_by_name(offer_name)
    logger.debug("Matching offers: %s", matching_offers)
    if len(matching_offers) == 0:
        raise OfferNotFoundError(f"Offer {offer_name} not found")
    best_matching_offer = find_best_offer_from_list(matching_offers)
    return best_matching_offer
