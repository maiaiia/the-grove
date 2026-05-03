from sqlalchemy.orm import Session
from backend.src.model import Plant, PlantCategory, PlantLocation
import datetime

class PlantRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def plants(self) -> list[Plant]:
        return self.db.query(Plant).order_by(Plant.id).all() #TODO - may want to order decr

    def __len__(self) -> int:
        return self.db.query(Plant).count()

    def save(self, plant: Plant) -> Plant:
        """Create or update a plant"""
        if plant.id is None or plant.id == 0:
            # New plant - add to session
            plant.id = None
            self.db.add(plant)
        else:
            # Existing plant - merge changes
            plant = self.db.merge(plant)

        self.db.commit()
        self.db.refresh(plant)
        return plant

    def delete_plant(self, plant_id: int) -> bool:
        plant = self.get_plant(plant_id)
        if plant:
            self.db.delete(plant)
            self.db.commit()
            return True
        return False

    def get_plant(self, plant_id: int) -> Plant | None:
        return self.db.query(Plant).filter(Plant.id == plant_id).first()
