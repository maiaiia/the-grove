import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.src.model.base import Base

IMAGE_FOLDER_PATH = 'backend/src/images/'

class PlantPhoto(Base):
    __tablename__ = 'plant_photos'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    caption = Column(String, default='')
    date = Column(Date, nullable=False, default=datetime.date.today)

    plant_id=Column(Integer, ForeignKey('plants.id'))
    plant=relationship('Plant', back_populates='photos')

    @property
    def url(self):
        #todo + / plant_id + / filename
        return f"{IMAGE_FOLDER_PATH}{self.filename}"
