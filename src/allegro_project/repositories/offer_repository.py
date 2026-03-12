from allegro_project.models.offer import Offer
from allegro_project.data.mock_offers import database


class OfferRepository:
    def __init__(self):
        self.data = database

    def get_all(self) -> list[Offer]:
        return [Offer.model_validate(offer) for offer in self.data.values()]

    def get_by_id(self, offer_id: int) -> Offer | None:
        offer = self.data.get(offer_id)
        if offer is None:
            return None
        return Offer.model_validate(offer)
