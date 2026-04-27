import datetime
import pytest

from backend.src.model import PlantCategory, PlantLocation
from backend.src.service.plant_validator import PlantValidator, PlantValidationError


class TestPlantValidator:

    # Name Validation Tests
    def test_validate_name_valid(self):
        PlantValidator.validate_name("Monstera")
        PlantValidator.validate_name("My Special Plant")
        PlantValidator.validate_name("A")

    def test_validate_name_empty(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_name("")
        assert exc_info.value.field == "name"
        assert "cannot be empty" in exc_info.value.message.lower()

    def test_validate_name_whitespace_only(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_name("   ")
        assert exc_info.value.field == "name"

    def test_validate_name_none(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_name(None)
        assert exc_info.value.field == "name"

    def test_validate_name_too_long(self):
        long_name = "A" * 101
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_name(long_name)
        assert exc_info.value.field == "name"
        assert "100" in exc_info.value.message

    # Latin Name Validation Tests
    def test_validate_latin_name_valid(self):
        PlantValidator.validate_latin_name("Monstera deliciosa")
        PlantValidator.validate_latin_name("Ficus retusa")

    def test_validate_latin_name_empty(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_latin_name("")
        assert exc_info.value.field == "latin_name"

    def test_validate_latin_name_too_short(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_latin_name("AB")
        assert exc_info.value.field == "latin_name"

    def test_validate_latin_name_too_long(self):
        long_name = "A" * 201
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_latin_name(long_name)
        assert exc_info.value.field == "latin_name"

    # Category Validation Tests
    def test_validate_category_valid(self):
        PlantValidator.validate_category(PlantCategory.BONSAI)
        PlantValidator.validate_category(PlantCategory.TROPICAL)
        PlantValidator.validate_category(PlantCategory.SUCCULENT)

    def test_validate_category_all_not_allowed(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_category(PlantCategory.ALL)
        assert exc_info.value.field == "category"
        assert "all" in exc_info.value.message.lower()

    def test_validate_category_none(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_category(None)
        assert exc_info.value.field == "category"

    # Location Validation Tests
    def test_validate_location_valid(self):
        PlantValidator.validate_location(PlantLocation.INDOORS)
        PlantValidator.validate_location(PlantLocation.OUTDOORS)
        PlantValidator.validate_location(PlantLocation.WINDOWSILL)

    def test_validate_location_none(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_location(None)
        assert exc_info.value.field == "location"

    # Date Planted Validation Tests
    def test_validate_date_planted_valid(self):
        PlantValidator.validate_date_planted(datetime.date.today())
        PlantValidator.validate_date_planted(datetime.date(2020, 1, 1))
        PlantValidator.validate_date_planted(datetime.date(2000, 6, 15))

    def test_validate_date_planted_future(self):
        future_date = datetime.date.today() + datetime.timedelta(days=1)
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_date_planted(future_date)
        assert exc_info.value.field == "date_planted"
        assert "future" in exc_info.value.message.lower()

    def test_validate_date_planted_too_old(self):
        ancient_date = datetime.date(1500, 1, 1)
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_date_planted(ancient_date)
        assert exc_info.value.field == "date_planted"

    def test_validate_date_planted_none(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_date_planted(None)
        assert exc_info.value.field == "date_planted"

    # Watering Schedule Validation Tests
    def test_validate_watering_schedule_valid(self):
        PlantValidator.validate_watering_schedule(1)
        PlantValidator.validate_watering_schedule(7)
        PlantValidator.validate_watering_schedule(30)
        PlantValidator.validate_watering_schedule(365)

    def test_validate_watering_schedule_too_low(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_watering_schedule(0)
        assert exc_info.value.field == "watering_schedule"

    def test_validate_watering_schedule_too_high(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_watering_schedule(366)
        assert exc_info.value.field == "watering_schedule"

    def test_validate_watering_schedule_none(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_watering_schedule(None)
        assert exc_info.value.field == "watering_schedule"

    # Last Watered Validation Tests
    def test_validate_last_watered_valid(self):
        planted = datetime.date(2020, 1, 1)
        PlantValidator.validate_last_watered(datetime.date.today(), planted)
        PlantValidator.validate_last_watered(datetime.date(2020, 6, 1), planted)
        PlantValidator.validate_last_watered(planted, planted)  # Same day is OK

    def test_validate_last_watered_future(self):
        planted = datetime.date(2020, 1, 1)
        future = datetime.date.today() + datetime.timedelta(days=1)
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_last_watered(future, planted)
        assert exc_info.value.field == "last_watered"
        assert "future" in exc_info.value.message.lower()

    def test_validate_last_watered_before_planted(self):
        planted = datetime.date(2020, 1, 1)
        before = datetime.date(2019, 12, 31)
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_last_watered(before, planted)
        assert exc_info.value.field == "last_watered"
        assert "before" in exc_info.value.message.lower()

    def test_validate_last_watered_none(self):
        planted = datetime.date(2020, 1, 1)
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_last_watered(None, planted)
        assert exc_info.value.field == "last_watered"

    # Notes Validation Tests
    def test_validate_notes_valid(self):
        PlantValidator.validate_notes("This is a note")
        PlantValidator.validate_notes("")
        PlantValidator.validate_notes(None)
        PlantValidator.validate_notes("A" * 2000)

    def test_validate_notes_too_long(self):
        long_notes = "A" * 2001
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_notes(long_notes)
        assert exc_info.value.field == "notes"

    # Photos Validation Tests
    def test_validate_photos_valid(self):
        PlantValidator.validate_photos([])
        PlantValidator.validate_photos([1, 2, 3])
        PlantValidator.validate_photos([i for i in range(100)])

    def test_validate_photos_too_many(self):
        too_many = [i for i in range(101)]
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_photos(too_many)
        assert exc_info.value.field == "photos"

    # Complete Plant Validation Tests
    def test_validate_plant_create_all_valid(self):
        PlantValidator.validate_plant_create(
            name="Monstera",
            latin_name="Monstera deliciosa",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.WINDOWSILL,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )

    def test_validate_plant_create_invalid_name(self):
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_plant_create(
                name="",
                latin_name="Monstera deliciosa",
                category=PlantCategory.TROPICAL,
                location=PlantLocation.WINDOWSILL,
                date_planted=datetime.date(2020, 1, 1),
                watering_schedule=7
            )
        assert exc_info.value.field == "name"

    def test_validate_plant_update_all_valid(self):
        planted = datetime.date(2020, 1, 1)
        PlantValidator.validate_plant_update(
            name="Monstera",
            latin_name="Monstera deliciosa",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.WINDOWSILL,
            date_planted=planted,
            watering_schedule=7,
            last_watered=datetime.date(2020, 6, 1),
            notes="Some notes",
            photos=[1, 2, 3]
        )

    def test_validate_plant_update_invalid_last_watered(self):
        planted = datetime.date(2020, 1, 1)
        with pytest.raises(PlantValidationError) as exc_info:
            PlantValidator.validate_plant_update(
                name="Monstera",
                latin_name="Monstera deliciosa",
                category=PlantCategory.TROPICAL,
                location=PlantLocation.WINDOWSILL,
                date_planted=planted,
                watering_schedule=7,
                last_watered=datetime.date(2019, 12, 31),  # Before planted
                notes="Some notes",
                photos=[]
            )
        assert exc_info.value.field == "last_watered"