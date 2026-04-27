from fastapi import APIRouter
from backend.src.schema import StatisticsResponse
from backend.src.service import plant_service

stats_router = APIRouter(prefix="/api/stats", tags=["stats"])

@stats_router.get("/", response_model=StatisticsResponse)
def get_statistics():
    stats_data = plant_service.get_statistics()
    return stats_data