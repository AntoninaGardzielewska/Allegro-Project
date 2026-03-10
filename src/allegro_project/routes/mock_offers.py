from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from allegro_project.models.offer import Offer
from allegro_project.services.mock_offer_client import get_offer_by_id, get_offers

router = APIRouter()


@router.get("/offers", response_model=list[Offer])
async def route_get_all_offers():
    try:
        return get_offers()
    except ValidationError:
        raise HTTPException(status_code=500, detail="Wrong data type in database")


@router.get("/offers/{offer_id}", response_model=Offer)
async def route_get_offer_by_id(offer_id: int):
    try:
        result = get_offer_by_id(offer_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Offer with given id not found")

        return result
    except ValidationError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Wrong data type: {e}. Cannot convert to Offer",
        )
