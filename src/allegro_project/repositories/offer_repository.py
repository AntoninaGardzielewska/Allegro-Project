from allegro_project.models.offer import Offer


class OfferRepository:
    def __init__(self, database):
        self.data = database.copy()

    def get_all(self) -> list[Offer]:
        return [Offer.model_validate(offer) for offer in self.data.values()]

    def get_by_id(self, offer_id: int) -> Offer | None:
        offer = self.data.get(offer_id)
        if offer is None:
            return None
        return Offer.model_validate(offer)
