from sqlalchemy.orm import Session
from backend.src.model import PlantPhoto

class PhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def photos(self) -> list[PlantPhoto]:
        return self.db.query(PlantPhoto).all()

    def __len__(self) -> int:
        return self.db.query(PlantPhoto).count()

    def save(self, photo: PlantPhoto) -> PlantPhoto:
        """Create or update a photo"""
        if photo.id is None or photo.id == 0:
            photo.id = None
            self.db.add(photo)
        else:
            photo = self.db.merge(photo)

        self.db.commit()
        self.db.refresh(photo)
        return photo

    def delete_photo(self, photo_id: int) -> bool:
        photo = self.get_photo(photo_id)
        if photo:
            self.db.delete(photo)
            self.db.commit()
            return True
        return False

    def get_photo(self, photo_id: int) -> PlantPhoto | None:
        return self.db.query(PlantPhoto).filter(PlantPhoto.id == photo_id).first()

    def get_photos_per_plant(self, plant_id: int) -> list[PlantPhoto]:
        return self.db.query(PlantPhoto).filter(PlantPhoto.plant_id == plant_id).order_by(PlantPhoto.date).all()

    def get_latest_photo_for_plant(self, plant_id: int) -> PlantPhoto | None:
        return (
            self.db.query(PlantPhoto)
            .filter(PlantPhoto.plant_id == plant_id)
            .order_by(PlantPhoto.id.desc())
            .first()
        )

    def delete_photos_for_plant(self, plant_id: int):
        """Delete all photos for a specific plant"""
        self.db.query(PlantPhoto).filter(PlantPhoto.plant_id == plant_id).delete()
        self.db.commit()