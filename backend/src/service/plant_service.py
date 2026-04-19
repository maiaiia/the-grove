from collections import Counter

from backend.src.model.plant import Plant
from backend.src.model.plant_photo import PlantPhoto
from backend.src.repository.plant_repository import PlantRepository, plant_repository
from backend.src.schema.plant_schema import PlantSummaryResponse, PlantPhotoResponse, PlantDetailResponse, \
    StatisticsResponse, EMPTY_STATS_RESPONSE, ChartItem


class PlantService:
    IMAGE_FOLDER_PATH = 'backend/src/images/'

    def __init__(self, repository: PlantRepository):
        self.__repository = repository

    def get_all_plants(self) -> list[PlantSummaryResponse]:
        plants = self.__repository.plants
        return [self._to_summary_response(plant) for plant in plants]

    def get_plant(self, plant_id: int) -> PlantDetailResponse:
        return PlantService._to_detail_response(self.__repository.get_plant(plant_id))

    def get_statistics(self) -> StatisticsResponse:
        total_plants = len(self.__repository)
        if total_plants == 0:
            return EMPTY_STATS_RESPONSE

        all_plants = self.__repository.plants
        oldest_plant = max(p.age for p in all_plants)
        total_photos = sum(len(p.photos) for p in all_plants if p.photos)
        unique_locations = len({p.location for p in all_plants if p.location})

        age_counts = {
            '<1y': 0,
            '1-2y': 0,
            '2-5y': 0,
            '5-10y': 0,
            '10-25y': 0,
            '25y+': 0
        }
        for p in all_plants:
            age = p.age
            if age < 1:
                age_counts['<1y'] += 1
            elif age <= 2:
                age_counts['1-2y'] += 1
            elif age <= 5:
                age_counts['2-5y'] += 1
            elif age <= 10:
                age_counts['5-10y'] += 1
            elif age <= 25:
                age_counts['10-25y'] += 1
            else:
                age_counts['25y+'] += 1

        photo_counts = Counter()
        for p in all_plants:
            count = len(p.photos) if p.photos else 0
            if count == 0:
                photo_counts['0 photos'] += 1
            elif 1 <= count <= 2:
                photo_counts['1-2 photos'] += 1
            elif 3 <= count <= 5:
                photo_counts['3-5 photos'] += 1
            elif 6 <= count <= 10:
                photo_counts['6-10 photos'] += 1
            else:
                photo_counts['10+ photos'] += 1

        water_counts = Counter()
        for p in all_plants:
            days = p.watering_schedule
            if days <= 2:
                water_counts['High (Every 1-2 days)'] += 1
            elif days <= 7:
                water_counts['Weekly'] += 1
            elif days <= 14:
                water_counts['Bi-Weekly'] += 1
            elif days <= 30:
                water_counts['Monthly'] += 1
            else:
                water_counts['Seasonal/Occasional'] += 1

        type_counts = Counter(p.category for p in all_plants)

        return StatisticsResponse(
            total_plants=total_plants,
            oldest_plant=oldest_plant,
            total_photos=total_photos,
            unique_locations=unique_locations,

            age_distribution=[ChartItem(label=k, count=v) for k, v in age_counts.items()],
            type_distribution=[ChartItem(label=k, count=v) for k, v in type_counts.items()],
            photo_distribution=[ChartItem(label=k, count=v) for k, v in photo_counts.items()],
            watering_distribution=[ChartItem(label=k, count=v) for k, v in water_counts.items()],
        )


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