from backend.src.model.plant import Plant
from backend.src.repository.plant_repository import PlantRepository


class PlantService:
    def __init__(self, repository: PlantRepository):
        self.__repository = repository

    def get_all_plants(self) -> list[Plant]:
        return self.__repository.plants

    def get_by_id(self, plant_id: int) -> Plant:
        return self.__repository.get_plant(plant_id)
