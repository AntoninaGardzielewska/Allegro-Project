from uuid import UUID

from fastapi import APIRouter

from src.services.mock_offer_client import get_offer_by_id, get_offers

router = APIRouter()


@router.get("/offers")
async def route_get_all_offers():
    return get_offers()


@router.get("/offers/{offer_id}")
async def route_get_offer_by_id(offer_id: UUID):
    print(get_offer_by_id(offer_id))
    return get_offer_by_id(offer_id)
