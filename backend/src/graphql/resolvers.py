import strawberry
from datetime import date
from typing import Optional
from backend.src.graphql.types import (
    PlantDetailType, PlantSummaryType, PlantPhotoType,
    StatisticsType, ChartItemType, PageResultType
)
from backend.src.service import plant_service

#region helpers

def _photo(p):
    return PlantPhotoType(
        id=p.id,
        plant_id=p.plant_id,
        url=p.url,
        caption=p.caption,
        date=p.date
    ) if p else None

def _summary(s) -> PlantSummaryType:
    return PlantSummaryType(
        id=s.id,
        name=s.name,
        latin_name=s.latin_name,
        category=s.category.value,
        last_watered=s.last_watered,
        age=s.age,
        image=_photo(s.image)
    )

def _detail(d) -> PlantDetailType:
    return PlantDetailType(
        id=d.id,
        name=d.name,
        latin_name=d.latin_name,
        category=d.category.value,
        last_watered=d.last_watered,
        age=d.age,
        image=_photo(d.image),
        location=d.location.value,
        date_planted=d.date_planted,
        photo_count=d.photo_count,
        watering_schedule=d.watering_schedule,
        notes=d.notes,
        photos=[PlantPhotoType(id=p.id, plant_id=p.plant_id, url=p.url, caption=p.caption, date=p.date)
                for p in d.photos]
    )

def _stats(s) -> StatisticsType:
    def chart(items): return [ChartItemType(label=i.label, count=i.count) for i in items]
    return StatisticsType(
        total_plants=s.total_plants, oldest_plant=s.oldest_plant,
        total_photos=s.total_photos, unique_locations=s.unique_locations,
        age_distribution=chart(s.age_distribution),
        type_distribution=chart(s.type_distribution),
        photo_distribution=chart(s.photo_distribution),
        watering_distribution=chart(s.watering_distribution),
        location_distribution=chart(s.location_distribution),
    )
#endregion

#region queries
@strawberry.type
class Query:
    @strawberry.field
    def plants(self) -> list[PlantSummaryType]:
        return [_summary(p) for p in plant_service.get_all_plants()]

    @strawberry.field
    def plants_page(self, page_number: int, plants_per_page: int) -> PageResultType:
        result = plant_service.get_plants_in_page(page_number, plants_per_page)
        return PageResultType(
            total=result.total,
            plants=[_summary(p) for p in result.plants]
        )

    @strawberry.field
    def plant(self, plant_id: int) -> Optional[PlantDetailType]:
        p = plant_service.get_plant(plant_id)
        return _detail(p) if p else None

    @strawberry.field
    def statistics(self) -> StatisticsType:
        return _stats(plant_service.get_statistics())

#endregion

#region input types

@strawberry.input
class PlantPhotoInput:
    url: str
    caption: str
    date: date

@strawberry.input
class CreatePlantInput:
    name: str
    latin_name: str
    category: str
    location: str
    date_planted: date
    watering_schedule: int

@strawberry.input
class UpdatePlantInput:
    name: str
    latin_name: str
    category: str
    location: str
    date_planted: date
    watering_schedule: int
    notes: str
    last_watered: date
    photos: list[PlantPhotoInput] #todo - remove

#endregion

#region mutations

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_plant(self, input: CreatePlantInput) -> PlantDetailType:
        from backend.src.schema.plant_schema import PlantCreateRequest
        from backend.src.model import PlantCategory, PlantLocation
        req = PlantCreateRequest(
            name=input.name, latin_name=input.latin_name,
            category=PlantCategory(input.category),
            location=PlantLocation(input.location),
            date_planted=input.date_planted,
            watering_schedule=input.watering_schedule,
        )
        return _detail(plant_service.create_plant(req))

    @strawberry.mutation
    def update_plant(self, plant_id: int, input: UpdatePlantInput) -> Optional[PlantDetailType]:
        from backend.src.schema.plant_schema import PlantUpdateRequest, PlantPhotoRequest
        req = PlantUpdateRequest(
            name=input.name, latin_name=input.latin_name,
            category=input.category, location=input.location,
            date_planted=input.date_planted,
            watering_schedule=input.watering_schedule,
            notes=input.notes, last_watered=input.last_watered,
            photos=[PlantPhotoRequest(url=p.url, caption=p.caption, date=p.date)
                    for p in input.photos],
        )
        result = plant_service.update_plant(plant_id, req)
        return _detail(result) if result else None

    @strawberry.mutation
    def delete_plant(self, plant_id: int) -> bool:
        plant_service.delete_plant(plant_id)
        return True

    @strawberry.mutation
    def add_plant_photo(
            self,
            plant_id: int,
            filename: str,
            caption: str
    ) -> PlantPhotoType:
        new_photo = plant_service.add_photo(
            plant_id=plant_id,
            filename=filename,
            caption=caption,
            date=date.today()
        )
        return _photo(new_photo)

    @strawberry.mutation
    def remove_plant_photo(self, photo_id: int) -> bool:
        return plant_service.delete_photo(photo_id)

#endregion