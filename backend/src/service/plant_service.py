from collections import Counter

from backend.src.model.plant import Plant
from backend.src.repository.plant_repository import PlantRepository, plant_repository
from backend.src.schema import PlantMapper, PlantSummaryResponse, PlantDetailResponse, StatisticsResponse, \
    EMPTY_STATS_RESPONSE, PlantCreateRequest


class PlantService:
    def __init__(self, repository: PlantRepository):
        self.__repository = repository

    def get_all_plants(self) -> list[PlantSummaryResponse]:
        plants = self.__repository.plants
        return [PlantMapper.to_summary_response(plant) for plant in plants]

    def get_plant(self, plant_id: int) -> PlantDetailResponse:
        return PlantMapper.to_detail_response(self.__repository.get_plant(plant_id))

    def get_statistics(self) -> StatisticsResponse:
        total_plants = len(self.__repository)
        if total_plants == 0:
            return EMPTY_STATS_RESPONSE

        all_plants = self.__repository.plants
        oldest_plant = max(p.age for p in all_plants)
        total_photos = sum(len(p.photos) for p in all_plants if p.photos)
        unique_locations = len({p.location for p in all_plants if p.location})

        age_counts = self._get_age_counts(all_plants)
        photo_counts = self._get_photo_counts(all_plants)
        water_counts = self._get_water_counts(all_plants)
        type_counts = Counter(p.category for p in all_plants)
        location_counts = Counter(p.location for p in all_plants)

        return PlantMapper.to_statistics_response(total_plants, oldest_plant, total_photos, unique_locations,
                               age_counts, type_counts, photo_counts, water_counts, location_counts)

    @staticmethod
    def _get_age_counts(all_plants: list[Plant]) -> {str: int}:
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
        return age_counts
    @staticmethod
    def _get_photo_counts(all_plants: list[Plant]) -> Counter:
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
        return photo_counts
    @staticmethod
    def _get_water_counts(all_plants: list[Plant]) -> Counter:
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
        return water_counts

    def create_plant(self, request: PlantCreateRequest):
        plant_model = PlantMapper.create_request_to_plant(request)
        saved_plant = self.__repository.save(plant_model)
        return PlantMapper.to_detail_response(saved_plant)

plant_service = PlantService(plant_repository)