from backend.src.model.plant import Plant
from backend.src.model.plant_photo import PlantPhoto
from backend.src.schema.plant_schema import PlantPhotoResponse, PlantSummaryResponse, PlantDetailResponse


class PlantMapper:
    IMAGE_FOLDER_PATH = 'backend/src/images/'
    @staticmethod
    def _get_photo_response(photo: PlantPhoto) -> PlantPhotoResponse:
        return PlantPhotoResponse(
            url=PlantMapper.IMAGE_FOLDER_PATH + photo.filename,
            description=photo.description,
            date=photo.date,
        )

    @staticmethod
    def _get_cover_photo(plant: Plant) -> PlantPhotoResponse:
        return PlantMapper._get_photo_response(plant.photos[-1]) if plant.photos and len(plant.photos) > 0 else None

    @staticmethod
    def to_summary_response(plant: Plant) -> PlantSummaryResponse:
        image = PlantMapper._get_cover_photo(plant)

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
    def to_detail_response(plant: Plant) -> PlantDetailResponse:
        image = PlantMapper._get_cover_photo(plant)
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
            photos=[PlantMapper._get_photo_response(photo) for photo in plant.photos],
        )