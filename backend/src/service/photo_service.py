import datetime

from backend.src.model import PlantPhoto
from backend.src.repository import PhotoRepository, photo_repository


class PhotoService:
    def __init__(self, repository: PhotoRepository):
        self.__repository = repository

    def __len__(self):
        return len(self.__repository)

    def add_photo(self, plant_id: int, filename: str, caption: str, date: datetime.date) -> PlantPhoto:
        photo = PlantPhoto(
            id=0,
            plant_id=plant_id,
            filename=filename,
            caption=caption,
            date=date,
        )
        return self.__repository.save(photo)

    def get_photo(self, photo_id: int) -> PlantPhoto:
        return self.__repository.get_photo(photo_id)

    def get_photos_per_plant(self, plant_id: int) -> list[PlantPhoto]:
        return self.__repository.get_photos_per_plant(plant_id)

    def get_photo_count(self, plant_id: int) -> int:
        #TODO - this can be optimized if the repo is modified to use a secondary index
        return len(self.get_photos_per_plant(plant_id))

    def get_latest_photo(self, plant_id: int) -> PlantPhoto or None:
        return self.__repository.get_latest_photo_for_plant(plant_id)

    def delete_photo(self, photo_id: int) -> bool:
        return self.__repository.delete_photo(photo_id)

    def delete_photos_for_plant(self, plant_id: int) -> bool:
        return self.__repository.delete_photos_for_plant(plant_id)

photo_service = PhotoService(photo_repository)