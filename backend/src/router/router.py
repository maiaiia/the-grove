from fastapi import APIRouter

from backend.src.schema.plant_schema import PlantSummaryResponse, PlantDetailResponse
from backend.src.service.plant_service import plant_service

plant_router = APIRouter(prefix="/api/plants", tags=["plants"])

@plant_router.get("/", response_model = list[PlantSummaryResponse])
def get_all_plants():
    return plant_service.get_all_plants()

@plant_router.get("/", response_model=PlantDetailResponse)
def get_plant(plant_id: int):
    return plant_service.get_plant(plant_id)