from fastapi import APIRouter, HTTPException

from backend.src.schema.plant_schema import PlantSummaryResponse, PlantDetailResponse
from backend.src.service.plant_service import plant_service

plant_router = APIRouter(prefix="/api/plants", tags=["plants"])

@plant_router.get("/", response_model = list[PlantSummaryResponse])
def get_all_plants():
    return plant_service.get_all_plants()

@plant_router.get("/{plant_id}", response_model=PlantDetailResponse)
def get_plant_detail(plant_id: int):
    plant = plant_service.get_plant(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant