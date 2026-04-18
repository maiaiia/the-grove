import datetime

from backend.model.plant_category import PlantCategory
from backend.model.plant_location import PlantLocation
from backend.model.plant_photo import PlantPhoto


class Plant:
    def __init__(
            self,
            plant_id: int,
            name: str,
            latin_name: str,
            category: PlantCategory,
            location: PlantLocation,
            date_planted: datetime.date,
            watering_schedule: int
    ):
        self.__id = plant_id
        self.__name = name
        self.__latin_name = latin_name
        self.__category = category
        self.__location = location
        self.__date_planted = date_planted
        self.__watering_schedule = watering_schedule
        self.__photos = []
        self.__last_watered = self.__date_planted
        self.__notes = ""

    #region Properties
    @property
    def id(self):
        return self.__id
    @property
    def name(self):
        return self.__name
    @property
    def latin_name(self):
        return self.__latin_name
    @property
    def category(self):
        return self.__category
    @property
    def location(self):
        return self.__location
    @property
    def date_planted(self):
        return self.__date_planted
    @property
    def watering_schedule(self):
        return self.__watering_schedule
    @property
    def photos(self):
        return self.__photos
    @property
    def last_watered(self):
        return self.__last_watered
    @property
    def notes(self):
        return self.__notes
    #endregion

    #region Setters
    @name.setter
    def name(self, new_name: str):
        self.__name = new_name
    @latin_name.setter
    def latin_name(self, new_name: str):
        self.__latin_name = new_name
    @category.setter
    def category(self, new_category: PlantCategory):
        self.__category = new_category
    @location.setter
    def location(self, new_location: PlantLocation):
        self.__location = new_location
    @date_planted.setter
    def date_planted(self, new_date_planted: datetime.date):
        self.__date_planted = new_date_planted
    @watering_schedule.setter
    def watering_schedule(self, new_watering_schedule: int):
        self.__watering_schedule = new_watering_schedule
    @notes.setter
    def notes(self, new_notes: str):
        self.__notes = new_notes
    #endregion

    def add_photo(self, photo_path: str, description: str):
        self.__photos.append(PlantPhoto(photo_path, description))
