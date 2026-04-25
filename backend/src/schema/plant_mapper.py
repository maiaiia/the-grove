from backend.src.model.plant import Plant
from backend.src.model.plant_photo import PlantPhoto
from backend.src.schema.plant_schema import PlantPhotoResponse, PlantSummaryResponse, PlantDetailResponse, \
    StatisticsResponse, ChartItem, PlantCreateRequest, PlantUpdateRequest, PlantPhotoRequest, PageRequestResponse


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
    def _get_photo_from_request(request: PlantPhotoRequest) -> PlantPhoto:
        return PlantPhoto(
            filename=request.url.split('/')[-1],
            description=request.description,
            date=request.date,
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

    @staticmethod
    def to_statistics_response(total_plants, oldest_plant, total_photos, unique_locations,
                               age_counts, type_counts, photo_counts, water_counts, location_counts) -> StatisticsResponse:
        return StatisticsResponse(
            total_plants=total_plants,
            oldest_plant=oldest_plant,
            total_photos=total_photos,
            unique_locations=unique_locations,

            age_distribution=[ChartItem(label=k, count=v) for k, v in age_counts.items()],
            type_distribution=[ChartItem(label=k, count=v) for k, v in type_counts.items()],
            photo_distribution=[ChartItem(label=k, count=v) for k, v in photo_counts.items()],
            watering_distribution=[ChartItem(label=k, count=v) for k, v in water_counts.items()],
            location_distribution=[ChartItem(label=k, count=v) for k, v in location_counts.items()]
        )

    @staticmethod
    def to_page_request_response(total_plants: int, plants_in_page: list[Plant]) -> PageRequestResponse:
        return PageRequestResponse(
            total=total_plants,
            plants= [] if plants_in_page is None else [PlantMapper.to_summary_response(plant) for plant in plants_in_page],
        )

    @staticmethod
    def create_request_to_plant(request: PlantCreateRequest) -> Plant:
        return Plant(
            id=0,
            name=request.name,
            latin_name=request.latin_name,
            category=request.category,
            location=request.location,
            date_planted=request.date_planted,
            watering_schedule=request.watering_schedule,
        )
    @staticmethod
    def update_request_to_plant(request: PlantUpdateRequest) -> Plant:
        return Plant(
            id=0,
            name=request.name,
            latin_name=request.latin_name,
            category=request.category,
            location=request.location,
            date_planted=request.date_planted,
            watering_schedule=request.watering_schedule,
            notes=request.notes,
            last_watered=request.last_watered,
            photos=[PlantMapper._get_photo_from_request(photo) for photo in request.photos],
        )