from dataclasses import dataclass, field
import datetime

from backend.src.model.enum.plant_category import PlantCategory
from backend.src.model.enum.plant_location import PlantLocation

@dataclass
class Plant:
    id:                 int
    name:               str
    latin_name:         str
    category:           PlantCategory
    location:           PlantLocation
    date_planted:       datetime.date
    watering_schedule:  int
    last_watered:       [datetime.date] = None
    notes:              str = ""

    def __post_init__(self):
        if self.last_watered is None:
            self.last_watered = self.date_planted

    @property
    def age(self) -> int:
        today = datetime.date.today()
        return (today - self.date_planted).days // 365

    def needs_watering(self) -> bool:
        days_since = (datetime.date.today() - self.last_watered).days
        return days_since >= self.watering_schedule

    def water(self):
        self.last_watered = datetime.date.today()