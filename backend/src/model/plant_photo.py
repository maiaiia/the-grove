import datetime

class PlantPhoto:
    def __init__(self, filename: str, description: str, date = datetime.date):
        self.__filename = filename
        self.__description = description
        self.__date = date

    @property
    def filename(self):
        return self.__filename
    @property
    def description(self):
        return self.__description
    @property
    def date(self):
        return self.__date

    @description.setter
    def description(self, description: str):
        self.__description = description