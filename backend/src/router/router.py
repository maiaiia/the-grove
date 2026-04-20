from fastapi import APIRouter, HTTPException
from starlette import status

from backend.src.schema.plant_schema import PlantSummaryResponse, PlantDetailResponse, StatisticsResponse, \
    PlantCreateRequest, PlantUpdateRequest
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

@plant_router.post(
    "/",
    response_model=PlantDetailResponse,
    status_code=status.HTTP_201_CREATED
)
def create_plant(request: PlantCreateRequest):
    new_plant = plant_service.create_plant(request)
    return new_plant

@plant_router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(plant_id: int):
    plant_service.delete_plant(plant_id)

@plant_router.put(
    "/{plant_id}",
    response_model=PlantDetailResponse
)
def update_plant(plant_id: int, request: PlantUpdateRequest):
    updated_plant = plant_service.update_plant(plant_id, request)
    if not updated_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return updated_plant

stats_router = APIRouter(prefix="/api/stats", tags=["stats"])

@stats_router.get("/", response_model=StatisticsResponse)
def get_statistics():
    stats_data = plant_service.get_statistics()
    return stats_data
