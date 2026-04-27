import datetime

from backend.src.model import PlantPhoto

class PhotoRepository:
    def __init__(self):
        self.__photos: dict[int: PlantPhoto] = {}
        self.__next_id: int = 1
        self.__add_mock_photos()

    @property
    def photos(self) -> list[PlantPhoto]:
        return list(self.__photos.values())
    def __len__(self) -> int:
        return len(self.__photos)

    def save(self, photo: PlantPhoto) -> PlantPhoto:
        if photo.id == 0:
            photo.id = self.__next_id
            self.__next_id += 1

        self.__photos[photo.id] = photo
        return self.__photos[photo.id]

    def delete_photo(self, photo_id: int) -> bool:
        #todo - should probably also delete the photo from the storage but given that i am working with in-memory stuff i'm not gonna do that
        if photo_id in self.__photos:
            del self.__photos[photo_id]
            return True
        return False

    def get_photo(self, photo_id: int) -> PlantPhoto:
        return self.__photos.get(photo_id)

    def get_photos_per_plant(self, plant_id: int) -> list[PlantPhoto]:
        return [photo for photo in self.__photos.values() if photo.plant_id == plant_id]

    def get_latest_photo_for_plant(self, plant_id: int) -> PlantPhoto or None:
        photos = self.get_photos_per_plant(plant_id)
        return None if photos is None or len(photos) == 0 else photos[-1] #TODO - prob needs some sorting too but i can't be bothered rn

    def delete_photos_for_plant(self, plant_id: int):
        to_delete = self.get_photos_per_plant(plant_id)
        for photo in to_delete:
            self.delete_photo(photo.id)

    def __add_mock_photos(self):
        photos = [
            PlantPhoto(
                id=0,
                plant_id=1,
                filename="monstera.jpg",
                caption="Looking particularly gorgeous today!",
                date=datetime.date(2024, 3, 2),
            ),
            PlantPhoto(
                id=0,
                plant_id=2,
                filename="oldjuniper.jpeg",
                caption="Oldie",
                date=datetime.date(2026, 3, 20),
            ),
            PlantPhoto(
                id=0,
                plant_id=3,
                filename="ficus.jpeg",
                caption="",
                date=datetime.date(2026, 3, 20),
            ),
            PlantPhoto(
                id=0,
                plant_id=4,
                filename="blackpine.jpeg",
                caption="Looking particularly gorgeous today!",
                date=datetime.date(2026, 3, 20),
            ),
            PlantPhoto(
                id=0,
                plant_id=5,
                filename="ghostorchid.jpeg",
                caption="Looking particularly gorgeous today!",
                date=datetime.date(2026, 3, 20),
            ),
            PlantPhoto(
                id=0,
                plant_id=6,
                filename="aloevera.jpeg",
                caption="Looking particularly gorgeous today!",
                date=datetime.date(2026, 3, 20),
            ),
        ]
        for photo in photos:
            self.save(photo)

photo_repository = PhotoRepository()