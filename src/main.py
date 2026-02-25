from fastapi import FastAPI

from src.routes.health import router as health_router
from src.routes.mock_offers import router as mock_offer_router

app = FastAPI()

app.include_router(health_router)
app.include_router(mock_offer_router)
