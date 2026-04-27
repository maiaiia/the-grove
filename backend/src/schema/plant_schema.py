from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from backend.src.model import PlantCategory, PlantLocation

class BaseModelWithCaseConversion(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class PhotoBase(BaseModelWithCaseConversion):
    id:         int
    plant_id:   int
    url:        str
    caption:    str
    date:       date

class PlantPhotoRequest(PhotoBase):
    pass
class PlantPhotoResponse(PhotoBase):
    pass

class PlantSummaryResponse(BaseModelWithCaseConversion):
    id:             int
    name:           str
    latin_name:     str
    category:       PlantCategory
    last_watered:   date
    age:            int
    image:          PlantPhotoResponse | None
    #needs_watering: bool

class PageRequestResponse(BaseModelWithCaseConversion):
    plants: list[PlantSummaryResponse]
    total:  int

class PlantDetailResponse(PlantSummaryResponse):
    location:           PlantLocation
    date_planted:       date
    photo_count:        int
    watering_schedule:  int
    notes:              str
    photos:             list[PlantPhotoResponse]

class ChartItem(BaseModelWithCaseConversion):
    label: str
    count: int

class StatisticsResponse(BaseModelWithCaseConversion):
    total_plants:       int
    oldest_plant:       int
    total_photos:       int
    unique_locations:   int

    age_distribution:       list[ChartItem]
    type_distribution:      list[ChartItem]
    photo_distribution:     list[ChartItem]
    watering_distribution:  list[ChartItem]
    location_distribution:  list[ChartItem]

EMPTY_STATS_RESPONSE = StatisticsResponse(
    total_plants=0,
    oldest_plant=0,
    total_photos=0,
    unique_locations=0,
    age_distribution=[],
    type_distribution=[],
    photo_distribution=[],
    watering_distribution=[],
    location_distribution=[]
)

class PlantBase(BaseModelWithCaseConversion):
    name:               str
    latin_name:         str
    category:           PlantCategory
    location:           PlantLocation
    date_planted:       date
    watering_schedule:  int

class PlantCreateRequest(PlantBase):
    pass
class PlantUpdateRequest(PlantBase):
    notes:          str
    last_watered:   date
    photos:         list[PlantPhotoRequest]


#todo - plant detail response should not have an image.
# create a new schema that contains a plant detail response AND an image
# and name it something else




