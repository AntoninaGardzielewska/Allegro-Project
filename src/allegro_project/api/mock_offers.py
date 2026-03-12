from fastapi import APIRouter, HTTPException

from allegro_project.models.offer import Offer
from allegro_project.services.mock_offer_service import get_offer_by_id, get_offers
from allegro_project.utils.result import OfferNotFoundError

router = APIRouter()


@router.get("/offers", response_model=list[Offer])
async def route_get_all_offers():
    return get_offers()


@router.get("/offers/{offer_id}", response_model=Offer)
async def route_get_offer_by_id(offer_id: int):
    try:
        result = get_offer_by_id(offer_id)
        return result
    except OfferNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
