from backend.src.model import Plant, PlantPhoto
from backend.src.schema.plant_schema import PlantPhotoResponse, PlantSummaryResponse, PlantDetailResponse, \
    StatisticsResponse, ChartItem, PlantCreateRequest, PlantUpdateRequest, PlantPhotoRequest, PageRequestResponse


class PlantMapper:
    @staticmethod
    def _get_photo_response(photo: PlantPhoto or None) -> PlantPhotoResponse or None:
        if photo is None:
            return None
        return PlantPhotoResponse(
            id=photo.id,
            plant_id=photo.plant_id,
            url=photo.url,
            caption=photo.caption,
            date=photo.date,
        )
    @staticmethod
    def _get_photo_from_request(request: PlantPhotoRequest) -> PlantPhoto:
        #TODO - requests should have ids
        return PlantPhoto(
            id=request.id,
            plant_id=request.plant_id,
            filename=request.url.split('/')[-1],
            caption=request.caption,
            date=request.date,
        )

    @staticmethod
    def to_summary_response(plant: Plant, photo: PlantPhoto) -> PlantSummaryResponse:

        return PlantSummaryResponse(
            id=plant.id,
            name=plant.name,
            latin_name=plant.latin_name,
            category=plant.category.value,
            last_watered=plant.last_watered,
            age=plant.age,
            image=PlantMapper._get_photo_response(photo)
        )

    @staticmethod
    def to_detail_response(plant: Plant, photos: list[PlantPhoto]) -> PlantDetailResponse:
        return PlantDetailResponse(
            id=plant.id,
            name=plant.name,
            latin_name=plant.latin_name,
            category=plant.category.value,
            last_watered=plant.last_watered,
            age=plant.age,
            image= None if photos is None or len(photos) == 0 else PlantMapper._get_photo_response(photos[-1]),
            location=plant.location.value,
            date_planted=plant.date_planted,
            photo_count=len(photos),
            watering_schedule=plant.watering_schedule,
            notes=plant.notes,
            photos=[PlantMapper._get_photo_response(photo) for photo in photos],
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
    def to_page_request_response(total_plants: int, plants_in_page: dict[int:list[Plant, PlantPhoto]]) -> PageRequestResponse:
        return PageRequestResponse(
            total=total_plants,
            plants= [] if plants_in_page is None else [PlantMapper.to_summary_response(plant, photo) for plant, photo in plants_in_page.values()],
        )

    @staticmethod
    def create_request_to_plant(request: PlantCreateRequest) -> Plant:
        return Plant(
            name=request.name,
            latin_name=request.latin_name,
            category=request.category,
            location=request.location,
            date_planted=request.date_planted,
            last_watered=request.date_planted,
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
        )