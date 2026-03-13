from fastapi import APIRouter, HTTPException, Depends

from allegro_project.models.offer import Offer
from allegro_project.services.mock_offer_service import get_offer_by_id, get_offers
from allegro_project.utils.result import OfferNotFoundError
from allegro_project.data.mock_offers import database
from allegro_project.repositories.offer_repository import OfferRepository

router = APIRouter()


def get_repository():
    return OfferRepository(database)


@router.get("/offers", response_model=list[Offer])
async def route_get_all_offers(repository=Depends(get_repository)):
    return get_offers(repository)


@router.get("/offers/{offer_id}", response_model=Offer)
async def route_get_offer_by_id(offer_id: int, repository=Depends(get_repository)):
    try:
        return get_offer_by_id(offer_id, repository)
    except OfferNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
