from datetime import date
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from backend.src.model.plant_category import PlantCategory
from backend.src.model.plant_location import PlantLocation

class BaseModelWithCaseConversion(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class PlantPhotoResponse(BaseModelWithCaseConversion):
    url: str
    description: str
    date: date

class PlantSummaryResponse(BaseModelWithCaseConversion):
    id: int
    name: str
    latin_name: str
    category: PlantCategory
    last_watered: date
    age: int
    image: PlantPhotoResponse | None
    #needs_watering: bool


class PlantDetailResponse(PlantSummaryResponse):
    location: PlantLocation
    date_planted: date
    photo_count: int
    watering_schedule: int
    notes: str
    photos: list[PlantPhotoResponse]
