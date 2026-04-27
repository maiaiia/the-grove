import datetime
from dataclasses import dataclass

IMAGE_FOLDER_PATH = 'backend/src/images/'

@dataclass
class PlantPhoto:
    filename:   str
    caption:    str
    date:       datetime.date
    plant_id:   int = 0
    id:         int = 0

    @property
    def url(self):
        #todo + / plant_id + / filename
        return IMAGE_FOLDER_PATH + self.filename
