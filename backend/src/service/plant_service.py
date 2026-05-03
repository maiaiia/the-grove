import datetime
from collections import Counter

from sqlalchemy.orm import Session

from backend.src.model import Plant
from backend.src.repository import PlantRepository
from backend.src.schema import PlantMapper, PlantSummaryResponse, PlantDetailResponse, StatisticsResponse, \
    EMPTY_STATS_RESPONSE, PlantCreateRequest, PageRequestResponse
from backend.src.schema.plant_schema import PlantUpdateRequest
from backend.src.service.photo_service import PhotoService
from backend.src.service.plant_validator import PlantValidator


class PlantService:
    def __init__(self, db: Session):
        self.__repository = PlantRepository(db)
        self.__photo_service = PhotoService(db)

    def get_all_plants(self) -> list[PlantSummaryResponse]:
        plants = self.__repository.plants
        return [PlantMapper.to_summary_response(plant, self.__photo_service.get_latest_photo(plant.id)) for plant in plants]

    def get_plants_in_page(self, page_number: int, plants_per_page: int) -> PageRequestResponse:
        start = (page_number - 1) * plants_per_page
        end = min(page_number * plants_per_page, len(self.__repository.plants))

        total_plants = len(self.__repository)
        plants_in_page = [] if start >= end else self.__repository.plants[start:end]
        plants_and_thumbnails = {} if plants_in_page is [] \
            else {plant.id : [plant, self.__photo_service.get_latest_photo(plant.id)]
                  for plant in plants_in_page}
        return PlantMapper.to_page_request_response(total_plants, plants_and_thumbnails)

    def get_plant(self, plant_id: int) -> PlantDetailResponse:
        return PlantMapper.to_detail_response(
            self.__repository.get_plant(plant_id),
            self.__photo_service.get_photos_per_plant(plant_id)
        )

    def get_statistics(self) -> StatisticsResponse:
        total_plants = len(self.__repository)
        if total_plants == 0:
            return EMPTY_STATS_RESPONSE

        all_plants = self.__repository.plants
        oldest_plant = max(p.age for p in all_plants)
        total_photos = len(self.__photo_service) #TODO ugly
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
    def _get_photo_counts(self, all_plants: list[Plant]) -> Counter:
        photo_counts = Counter()
        for p in all_plants:
            count = self.__photo_service.get_photo_count(p.id)
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

        PlantValidator.validate_plant_create(
            name=request.name,
            latin_name=request.latin_name,
            category=request.category,
            location=request.location,
            date_planted=request.date_planted,
            watering_schedule=request.watering_schedule
        )
        plant_model = PlantMapper.create_request_to_plant(request)
        saved_plant = self.__repository.save(plant_model)
        return PlantMapper.to_detail_response(saved_plant, [])

    def delete_plant(self, plant_id: int):
        self.__repository.delete_plant(plant_id)
        self.__photo_service.delete_photos_for_plant(plant_id)

    #TODO - update request probably shouldn't include photos :))
    def update_plant(self, plant_id: int, request: PlantUpdateRequest):
        plant = self.__repository.get_plant(plant_id)
        if not plant:
            return None


        PlantValidator.validate_plant_update(
            name=request.name,
            latin_name=request.latin_name,
            category=request.category,
            location=request.location,
            date_planted=request.date_planted,
            watering_schedule=request.watering_schedule,
            last_watered=request.last_watered,
            notes=request.notes,
        )

        plant.name = request.name
        plant.latin_name = request.latin_name
        plant.category = request.category
        plant.location = request.location
        plant.date_planted = request.date_planted
        plant.watering_schedule = request.watering_schedule
        plant.notes = request.notes

        self.__repository.save(plant)
        #TODO - i suppose this should be a different type of response, because it really really shouldn't include the photos.
        # uhghghghghghhghgahahahglajsflkjh
        return PlantMapper.to_detail_response(plant, self.__photo_service.get_photos_per_plant(plant_id))

    def add_photo(self, plant_id: int, filename: str, caption: str, date: datetime.date):
        return self.__photo_service.add_photo(plant_id, filename, caption, date)
    def delete_photo(self, photo_id: int):
        return self.__photo_service.delete_photo(photo_id)