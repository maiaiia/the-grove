import datetime

class PlantPhoto:
    def __init__(self, filename: str, caption: str, date = datetime.date):
        self.__filename = filename
        self.__caption = caption
        self.__date = date

    @property
    def filename(self):
        return self.__filename
    @property
    def caption(self):
        return self.__caption
    @property
    def date(self):
        return self.__date

    @caption.setter
    def caption(self, caption: str):
        self.__caption = caption