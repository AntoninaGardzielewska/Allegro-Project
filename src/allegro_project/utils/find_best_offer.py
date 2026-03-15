from allegro_project.models.offer import Offer
import logging

logger = logging.getLogger(__name__)


def find_best_offer_from_list(offers: list[Offer]) -> Offer:
    best_offer = min(offers, key=lambda offer: offer.price)
    logger.debug(
        "Best offer found: %s with price %s", best_offer.name, best_offer.price
    )
    return best_offer
