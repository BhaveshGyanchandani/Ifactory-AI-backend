from fastapi import FastAPI

from power_plant.routes import router as power_router
from steel_plant.routes import router as steel_router

app = FastAPI()

app.include_router(
    power_router,
    prefix="/power"
)

app.include_router(
    steel_router,
    prefix="/steel"
)