from datetime import datetime
from pydantic import BaseModel

from backend.src.model.plant_category import PlantCategory
from backend.src.model.plant_location import PlantLocation


class PlantPhotoResponse(BaseModel):
    url: str
    description: str
    date: datetime.date


class PlantSummaryResponse(BaseModel):
    id: int
    name: str
    latin_name: str
    category: PlantCategory
    location: PlantLocation
    date_planted: datetime.date
    last_watered: datetime.date
    watering_schedule: int
    needs_watering: bool
    age_years: int
    photo_count: int
    cover_photo: PlantPhotoResponse | None  # first photo, if any


class PlantDetailResponse(PlantSummaryResponse):
    notes: str
    photos: list[PlantPhotoResponse]