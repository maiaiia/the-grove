from backend.src.model.plant import Plant
from backend.src.repository.plant_repository import PlantRepository, plant_repository
from backend.src.schema.plant_schema import PlantSummaryResponse, PlantPhotoResponse


class PlantService:
    IMAGE_FOLDER_PATH = 'backend/src/images/'

    def __init__(self, repository: PlantRepository):
        self.__repository = repository

    def get_all_plants(self) -> list[PlantSummaryResponse]:
        plants = self.__repository.plants
        return [self._to_summary_response(plant) for plant in plants]

    def get_plant(self, plant_id: int) -> Plant:
        return self.__repository.get_plant(plant_id)


    @staticmethod
    def _to_summary_response(plant: Plant) -> PlantSummaryResponse:
        image = None
        if plant.photos and len(plant.photos) > 0:
            image = plant.photos[-1]
            image = PlantPhotoResponse(
                url = PlantService.IMAGE_FOLDER_PATH + image.filename,
                description = image.description,
                date = image.date
            )
        return PlantSummaryResponse(
            id=plant.id,
            name=plant.name,
            latin_name=plant.latin_name,
            category=plant.category.value,
            last_watered=plant.last_watered,
            age=plant.age,
            image=image
        )

plant_service = PlantService(plant_repository)