from dataclasses import dataclass, field
import datetime

from backend.model.plant_category import PlantCategory
from backend.model.plant_location import PlantLocation
from backend.model.plant_photo import PlantPhoto


@dataclass
class Plant:
    """Plant domain model using dataclass"""
    id: int
    name: str
    latin_name: str
    category: PlantCategory
    location: PlantLocation
    date_planted: datetime.date
    watering_schedule: int
    photos: list[PlantPhoto]= field(default_factory=list)
    last_watered: [datetime.date] = None
    notes: str = ""

    def __post_init__(self):
        """Called after __init__"""
        if self.last_watered is None:
            self.last_watered = self.date_planted

    @property
    def age_years(self) -> int:
        today = datetime.date.today()
        return (today - self.date_planted).days // 365

    @property
    def photo_count(self) -> int:
        return len(self.photos)

    def needs_watering(self) -> bool:
        days_since = (datetime.date.today() - self.last_watered).days
        return days_since >= self.watering_schedule

    def water(self):
        self.last_watered = datetime.date.today()