import datetime

class PlantPhoto:
    def __init__(self, path: str, description: str):
        self.__path = path
        self.__description = description
        self.__date = datetime.date

    @property
    def path(self):
        return self.__path
    @property
    def description(self):
        return self.__description
    @property
    def date(self):
        return self.__date

    @description.setter
    def description(self, description: str):
        self.__description = description