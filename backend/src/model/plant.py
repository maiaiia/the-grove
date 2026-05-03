import datetime

from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from backend.src.model.base import Base

from backend.src.model.enum.plant_category import PlantCategory
from backend.src.model.enum.plant_location import PlantLocation

class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    latin_name = Column(String)
    category = Column(Enum(PlantCategory), nullable=False)
    location = Column(Enum(PlantLocation), nullable=False)
    date_planted = Column(Date, default=datetime.date.today)
    watering_schedule = Column(Integer)
    last_watered = Column(Date, nullable=True)
    notes = Column(String, default="")

    photos = relationship("PlantPhoto", back_populates="plant")

    @property
    def age(self) -> int:
        today = datetime.date.today()
        return (today - self.date_planted).days // 365

    def needs_watering(self) -> bool:
        days_since = (datetime.date.today() - self.last_watered).days
        return days_since >= self.watering_schedule

    def water(self):
        self.last_watered = datetime.date.today()