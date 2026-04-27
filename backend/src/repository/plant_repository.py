import datetime

from backend.src.model import Plant, PlantCategory, PlantLocation, PlantPhoto

class PlantRepository:
    def __init__(self):
        self.__plants: dict[int, Plant] = {}
        self.__next_id = 1
        self.__add_mock_plants()

    def __add_mock_plants(self):
        plants = [
            Plant(
                0,
                "Monstera Rex",
                "Monstera deliciosa",
                PlantCategory.TROPICAL,
                PlantLocation.WINDOWSILL,
                datetime.date(2023, 3, 1),
                2,
                datetime.date(2026, 3, 20),
                "Grew from a single node cutting. Now has over 12 large leaves with beautiful fenestration."
            ),
            Plant(
                0,
                "Old Juniper",
                "Juniperus chinensis",
                PlantCategory.BONSAI,
                PlantLocation.INDOORS,
                datetime.date(2014, 3, 1),
                2,
                datetime.date(2026, 3, 24),
                ""
            ),
            Plant(
                0,
                "Little Ficus",
                "Ficus retusa",
                PlantCategory.BONSAI,
                PlantLocation.INDOORS,
                datetime.date(2018, 3, 1),
                7,
                datetime.date(2026, 3, 21),
                ""
            ),
            Plant(
                0,
                "Black Pine",
                "Pinus thunbergii",
                PlantCategory.BONSAI,
                PlantLocation.OUTDOORS,
                datetime.date(2011, 3, 1),
                2,
                datetime.date(2026, 3, 21),
                ""
            ),
            Plant(
                0,
                "Ghost Orchid",
                "Phalaenopsis amabilis",
                PlantCategory.FLOWERING,
                PlantLocation.INDOORS,
                datetime.date(2024, 3, 1),
                7,
                datetime.date(2026, 3, 21),
                ""
            ),
            Plant(
                0,
                "Aloe Vera",
                "Aloe vera",
                PlantCategory.SUCCULENT,
                PlantLocation.OUTDOORS,
                datetime.date(2021, 3, 1),
                14,
                datetime.date(2026, 3, 21),
                ""
            )
        ]
        for plant in plants:
            self.save(plant)

    @property
    def plants(self):
        return list(self.__plants.values())

    def __len__(self):
        return len(self.__plants)

    def save(self, plant: Plant) -> Plant:
        if plant.id == 0:
            plant.id = self.__next_id
            self.__next_id += 1
        self.__plants[plant.id] = plant
        return self.__plants[plant.id]

    def delete_plant(self, plant_id: int) -> bool:
        if plant_id in self.__plants:
            del self.__plants[plant_id]
            return True
        return False

    def get_plant(self, plant_id: int) -> Plant | None:
        return self.__plants.get(plant_id)

plant_repository = PlantRepository()