from fastapi import APIRouter
from sqlalchemy.orm import Session
from strawberry.types import info

from backend.src.schema import StatisticsResponse
from backend.src.service import PlantService

stats_router = APIRouter(prefix="/api/stats", tags=["stats"])

@stats_router.get("/", response_model=StatisticsResponse)
def get_statistics():
    db: Session = info.context["db"]
    plant_service = PlantService(db)
    stats_data = plant_service.get_statistics()
    return stats_data