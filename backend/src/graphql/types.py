import strawberry
from datetime import date
from typing import Optional

@strawberry.type
class PlantPhotoType:
    id: int
    plant_id: int
    url: str
    caption: str
    date: date

@strawberry.type
class PlantSummaryType:
    id: int
    name: str
    latin_name: str
    category: str
    last_watered: date
    age: int
    image: Optional[PlantPhotoType]

@strawberry.type
class PlantDetailType:
    id: int
    name: str
    latin_name: str
    category: str
    last_watered: date
    age: int
    image: Optional[PlantPhotoType]
    location: str
    date_planted: date
    photo_count: int
    watering_schedule: int
    notes: str
    photos: list[PlantPhotoType]

@strawberry.type
class ChartItemType:
    label: str
    count: int

@strawberry.type
class StatisticsType:
    total_plants: int
    oldest_plant: int
    total_photos: int
    unique_locations: int
    age_distribution: list[ChartItemType]
    type_distribution: list[ChartItemType]
    photo_distribution: list[ChartItemType]
    watering_distribution: list[ChartItemType]
    location_distribution: list[ChartItemType]

@strawberry.type
class PageResultType:
    total: int
    plants: list[PlantSummaryType]