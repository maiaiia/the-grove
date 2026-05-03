from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from strawberry.types import info

from backend.src.schema import PageRequestResponse
from backend.src.schema.plant_schema import PlantSummaryResponse, PlantDetailResponse, \
    PlantCreateRequest, PlantUpdateRequest
from backend.src.service import PlantService

plant_router = APIRouter(prefix="/api/plants", tags=["plants"])

@plant_router.get("/", response_model = list[PlantSummaryResponse])
def get_all_plants():
    db: Session = info.context["db"]
    plant_service = PlantService(db)
    return plant_service.get_all_plants()

@plant_router.get('/page/{page_number}', response_model = PageRequestResponse)
def get_plants_in_page(page_number: int, plants_per_page: int):
    db: Session = info.context["db"]
    plant_service = PlantService(db)
    return plant_service.get_plants_in_page(page_number, plants_per_page)

@plant_router.get("/{plant_id}", response_model=PlantDetailResponse)
def get_plant_detail(plant_id: int):
    db: Session = info.context["db"]
    plant_service = PlantService(db)
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
    db: Session = info.context["db"]
    plant_service = PlantService(db)
    new_plant = plant_service.create_plant(request)
    return new_plant

@plant_router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(plant_id: int):
    db: Session = info.context["db"]
    plant_service = PlantService(db)
    plant_service.delete_plant(plant_id)

@plant_router.put(
    "/{plant_id}",
    response_model=PlantDetailResponse
)
def update_plant(plant_id: int, request: PlantUpdateRequest):
    db: Session = info.context["db"]
    plant_service = PlantService(db)
    updated_plant = plant_service.update_plant(plant_id, request)
    if not updated_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return updated_plant
