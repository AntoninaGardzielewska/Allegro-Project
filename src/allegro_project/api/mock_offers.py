import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from allegro_project.data.mock_offers import database
from allegro_project.models.offer import Offer
from allegro_project.repositories.offer_repository import OfferRepository
from allegro_project.services.mock_offer_service import (
    find_best_offer_by_name,
    get_offer_by_id,
    get_offers,
)
from allegro_project.utils.result import OfferNotFoundError

logger = logging.getLogger(__name__)


router = APIRouter()


def get_repository():
    return OfferRepository(database)


@router.get("/offers", response_model=list[Offer])
async def route_get_all_offers(repository=Depends(get_repository)):
    """
    Retrieve all available offers.

    Args:
        repository (OfferRepository): Injected repository instance.

    Returns:
        list[Offer]: List of all available offers.
    """

    return await get_offers(repository)


@router.get("/offers/{offer_id}", response_model=Offer)
async def route_get_offer_by_id(offer_id: int, repository=Depends(get_repository)):
    """
    Retrieve an offer by its unique ID.

    Args:
        offer_id (int): Identifier of the offer.
        repository (OfferRepository): Injected repository instance.

    Returns:
        Offer: The requested offer.

    Raises:
        HTTPException: If the offer does not exist.
    """
    try:
        return await get_offer_by_id(offer_id, repository)
    except OfferNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/best_price/", response_model=Offer)
async def route_get_best_offer_by_name(
    offer_name: str = Query(min_length=1, max_length=100),
    repository=Depends(get_repository),
):
    """
    Retrieve the cheapest offer matching the given name.

    Args:
        offer_name (str): Name or partial name of the offer.
        repository (OfferRepository): Injected repository instance.

    Returns:
        Offer: The cheapest matching offer.

    Raises:
        HTTPException: If no matching offers are found.
    """

    logger.debug("Search best offer for: %s", offer_name)

    try:
        return await find_best_offer_by_name(offer_name, repository)
    except OfferNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
