from allegro_project.models.offer import Offer


class OfferRepository:
    def __init__(self, database):
        self.data = database

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
