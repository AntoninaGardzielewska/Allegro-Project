from allegro_project.models.offer import Offer

from allegro_project.data.mock_offers import database


def get_offers() -> list[Offer]:
    res: list[Offer] = []
    res = [Offer.model_validate(offer) for offer in database.values()]
    return res


def get_offer_by_id(offer_id: int) -> Offer | None:
    offer = database.get(offer_id)
    if offer is None:
        return None
    return Offer.model_validate(offer)
