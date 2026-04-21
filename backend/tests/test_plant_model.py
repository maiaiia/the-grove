"""
Tests for Plant model
"""
import datetime
import pytest

from backend.src.model.plant import Plant
from backend.src.model.plant_category import PlantCategory
from backend.src.model.plant_location import PlantLocation
from backend.src.model.plant_photo import PlantPhoto


class TestPlantModel:
    """Test suite for Plant model"""

    @pytest.fixture
    def sample_plant(self):
        """Create a sample plant for testing"""
        return Plant(
            id=1,
            name="Test Plant",
            latin_name="Testus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            photos=[],
            last_watered=None,  # Will be set by __post_init__
            notes="Test notes"
        )

    def test_plant_initialization(self):
        """Plant should initialize with all required fields"""
        plant = Plant(
            id=1,
            name="Monstera",
            latin_name="Monstera deliciosa",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.WINDOWSILL,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )

        assert plant.id == 1
        assert plant.name == "Monstera"
        assert plant.latin_name == "Monstera deliciosa"
        assert plant.category == PlantCategory.TROPICAL
        assert plant.location == PlantLocation.WINDOWSILL
        assert plant.watering_schedule == 7

    def test_plant_post_init_sets_last_watered(self):
        """__post_init__ should set last_watered to date_planted if None"""
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=None
        )

        assert plant.last_watered == datetime.date(2020, 1, 1)

    def test_plant_post_init_preserves_last_watered(self):
        """__post_init__ should not override existing last_watered"""
        custom_date = datetime.date(2020, 6, 1)
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=custom_date
        )

        assert plant.last_watered == custom_date

    def test_plant_age_property(self):
        """Age property should calculate correct age in years"""
        years_ago_3 = datetime.date.today() - datetime.timedelta(days=3 * 365 + 100)
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=years_ago_3,
            watering_schedule=7
        )

        assert plant.age == 3

    def test_plant_age_less_than_year(self):
        """Age property should return 0 for plants less than 1 year old"""
        recent = datetime.date.today() - datetime.timedelta(days=180)
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=recent,
            watering_schedule=7
        )

        assert plant.age == 0

    def test_plant_photo_count_empty(self):
        """Photo count should be 0 for empty photos list"""
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            photos=[]
        )

        assert plant.photo_count == 0

    def test_plant_photo_count_with_photos(self):
        """Photo count should match number of photos"""
        photos = [
            PlantPhoto("photo1.jpg", "First", datetime.date(2020, 1, 1)),
            PlantPhoto("photo2.jpg", "Second", datetime.date(2020, 2, 1)),
            PlantPhoto("photo3.jpg", "Third", datetime.date(2020, 3, 1)),
        ]
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            photos=photos
        )

        assert plant.photo_count == 3

    def test_needs_watering_true(self):
        """needs_watering should return True when watering is overdue"""
        past_date = datetime.date.today() - datetime.timedelta(days=10)
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=past_date
        )

        assert plant.needs_watering() is True

    def test_needs_watering_false(self):
        """needs_watering should return False when watering is not due"""
        recent_date = datetime.date.today() - datetime.timedelta(days=3)
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=recent_date
        )

        assert plant.needs_watering() is False

    def test_needs_watering_exact_day(self):
        """needs_watering should return True on exact day of schedule"""
        exact_date = datetime.date.today() - datetime.timedelta(days=7)
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=exact_date
        )

        assert plant.needs_watering() is True

    def test_water_method(self):
        """water() method should update last_watered to today"""
        past_date = datetime.date.today() - datetime.timedelta(days=10)
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=past_date
        )

        plant.water()

        assert plant.last_watered == datetime.date.today()
        assert plant.needs_watering() is False

    def test_plant_default_values(self):
        """Plant should have correct default values"""
        plant = Plant(
            id=1,
            name="Test",
            latin_name="Testus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )

        assert plant.photos == []
        assert plant.notes == ""
        assert plant.last_watered == datetime.date(2020, 1, 1)