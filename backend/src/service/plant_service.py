from backend.src.model.plant import Plant
from backend.src.model.plant_photo import PlantPhoto
from backend.src.repository.plant_repository import PlantRepository, plant_repository
from backend.src.schema.plant_schema import PlantSummaryResponse, PlantPhotoResponse, PlantDetailResponse


class PlantService:
    IMAGE_FOLDER_PATH = 'backend/src/images/'

    def __init__(self, repository: PlantRepository):
        self.__repository = repository

    def get_all_plants(self) -> list[PlantSummaryResponse]:
        plants = self.__repository.plants
        return [self._to_summary_response(plant) for plant in plants]

    def get_plant(self, plant_id: int) -> PlantDetailResponse:
        return PlantService._to_detail_response(self.__repository.get_plant(plant_id))

    @staticmethod
    def _get_photo_response(photo: PlantPhoto) -> PlantPhotoResponse:
        return PlantPhotoResponse(
            url=PlantService.IMAGE_FOLDER_PATH + photo.filename,
            description=photo.description,
            date=photo.date,
        )

    @staticmethod
    def _get_cover_photo(plant: Plant) -> PlantPhotoResponse:
        return PlantService._get_photo_response(plant.photos[-1]) if plant.photos and len(plant.photos) > 0 else None

    @staticmethod
    def _to_summary_response(plant: Plant) -> PlantSummaryResponse:
        image = PlantService._get_cover_photo(plant)

        return PlantSummaryResponse(
            id=plant.id,
            name=plant.name,
            latin_name=plant.latin_name,
            category=plant.category.value,
            last_watered=plant.last_watered,
            age=plant.age,
            image=image
        )

    @staticmethod
    def _to_detail_response(plant: Plant) -> PlantDetailResponse:
        image = PlantService._get_cover_photo(plant)
        return PlantDetailResponse(
            id=plant.id,
            name=plant.name,
            latin_name=plant.latin_name,
            category=plant.category.value,
            last_watered=plant.last_watered,
            age=plant.age,
            image=image,
            location=plant.location.value,
            date_planted=plant.date_planted,
            photo_count=plant.photo_count,
            watering_schedule=plant.watering_schedule,
            notes=plant.notes,
            photos=[PlantService._get_photo_response(photo) for photo in plant.photos],
        )

plant_service = PlantService(plant_repository)