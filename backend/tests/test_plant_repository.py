"""
Tests for PlantRepository
"""
import datetime
import pytest

from backend.src.model.plant import Plant
from backend.src.model.plant_category import PlantCategory
from backend.src.model.plant_location import PlantLocation
from backend.src.repository.plant_repository import PlantRepository


class TestPlantRepository:
    """Test suite for PlantRepository"""

    @pytest.fixture
    def empty_repository(self):
        repo = PlantRepository()
        # Clear mock data
        repo._PlantRepository__plants = {}
        repo._PlantRepository__next_id = 1
        return repo

    @pytest.fixture
    def sample_plant(self):
        return Plant(
            id=0,
            name="Test Plant",
            latin_name="Testus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            photos=[],
            last_watered=datetime.date(2020, 1, 1),
            notes="Test notes"
        )

    def test_repository_initialization(self):
        repo = PlantRepository()
        assert len(repo) > 0
        assert len(repo.plants) > 0

    def test_save_new_plant(self, empty_repository, sample_plant):
        saved = empty_repository.save(sample_plant)

        assert saved.id == 1
        assert len(empty_repository) == 1
        assert saved.name == "Test Plant"

    def test_save_multiple_plants(self, empty_repository):
        plant1 = Plant(
            id=0,
            name="Plant 1",
            latin_name="Plantus one",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )
        plant2 = Plant(
            id=0,
            name="Plant 2",
            latin_name="Plantus two",
            category=PlantCategory.BONSAI,
            location=PlantLocation.OUTDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=14
        )

        saved1 = empty_repository.save(plant1)
        saved2 = empty_repository.save(plant2)

        assert saved1.id == 1
        assert saved2.id == 2
        assert len(empty_repository) == 2

    def test_save_existing_plant(self, empty_repository, sample_plant):
        saved = empty_repository.save(sample_plant)
        original_id = saved.id

        saved.name = "Updated Name"
        updated = empty_repository.save(saved)

        assert updated.id == original_id
        assert updated.name == "Updated Name"
        assert len(empty_repository) == 1

    def test_get_plant_existing(self, empty_repository, sample_plant):
        saved = empty_repository.save(sample_plant)
        retrieved = empty_repository.get_plant(saved.id)

        assert retrieved is not None
        assert retrieved.id == saved.id
        assert retrieved.name == saved.name

    def test_get_plant_non_existing(self, empty_repository):
        retrieved = empty_repository.get_plant(999)
        assert retrieved is None

    def test_delete_plant_existing(self, empty_repository, sample_plant):
        saved = empty_repository.save(sample_plant)
        result = empty_repository.delete_plant(saved.id)

        assert result is True
        assert len(empty_repository) == 0
        assert empty_repository.get_plant(saved.id) is None

    def test_delete_plant_non_existing(self, empty_repository):
        """Deleting a non-existing plant should return False"""
        result = empty_repository.delete_plant(999)
        assert result is False

    def test_plants_property(self, empty_repository):
        plant1 = Plant(
            id=0,
            name="Plant 1",
            latin_name="Plantus one",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )
        plant2 = Plant(
            id=0,
            name="Plant 2",
            latin_name="Plantus two",
            category=PlantCategory.BONSAI,
            location=PlantLocation.OUTDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=14
        )

        empty_repository.save(plant1)
        empty_repository.save(plant2)

        all_plants = empty_repository.plants
        assert len(all_plants) == 2
        assert isinstance(all_plants, list)

    def test_len_operator(self, empty_repository, sample_plant):
        assert len(empty_repository) == 0

        empty_repository.save(sample_plant)
        assert len(empty_repository) == 1

    def test_mock_plants_have_correct_structure(self):
        repo = PlantRepository()

        for plant in repo.plants:
            assert plant.id > 0
            assert plant.name
            assert plant.latin_name
            assert isinstance(plant.category, PlantCategory)
            assert isinstance(plant.location, PlantLocation)
            assert isinstance(plant.date_planted, datetime.date)
            assert plant.watering_schedule > 0
            assert isinstance(plant.photos, list)
            assert isinstance(plant.last_watered, datetime.date)
            assert isinstance(plant.notes, str)