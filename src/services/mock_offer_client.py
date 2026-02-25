import json
from uuid import UUID

from pydantic import ValidationError

from src.models.offer import Offer

PATH_TO_DATA = "src/data/mock_offers.json"


# TODO: error handler with appropriate message
def get_offers():
    with open(PATH_TO_DATA) as json_file:
        res: list[Offer] = []
        offers_data = json.load(json_file)
        for offer in offers_data:
            try:
                new_offer = Offer.model_validate(offer)
                res.append(new_offer)
            except ValidationError as e:
                print(e)
        return res


# TODO: improve finding right offer
# TODO: fix wrong check for id
def get_offer_by_id(id: UUID):
    with open(PATH_TO_DATA) as json_file:
        offers_data = json.load(json_file)
        print(id, " id")
        for offer in offers_data:
            print(offer["id"])
            if offer["id"] == id:
                print("OK")
                try:
                    return Offer.model_validate(offer)
                except ValidationError as e:
                    print(e)
    return None
