import logging

from fastapi import FastAPI

from allegro_project.api.health import router as health_router
from allegro_project.api.mock_offers import router as mock_offer_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    filename="app.log",
    filemode="a",
    force=True,
)
app = FastAPI()

app.include_router(health_router)
app.include_router(mock_offer_router)
