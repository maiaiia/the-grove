"""
Server-side validation for plant data.
Validates business rules and data integrity.
"""
import datetime
from typing import Optional

from backend.src.model.plant_category import PlantCategory
from backend.src.model.plant_location import PlantLocation


class PlantValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class PlantValidator:
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 100
    MIN_LATIN_NAME_LENGTH = 3
    MAX_LATIN_NAME_LENGTH = 200
    MAX_NOTES_LENGTH = 2000
    MIN_WATERING_DAYS = 1
    MAX_WATERING_DAYS = 365
    MAX_PHOTOS_PER_PLANT = 100

    @staticmethod
    def validate_name(name: str) -> None:
        if not name or not name.strip():
            raise PlantValidationError("name", "Name cannot be empty")

        if len(name) < PlantValidator.MIN_NAME_LENGTH:
            raise PlantValidationError("name", f"Name must be at least {PlantValidator.MIN_NAME_LENGTH} character")

        if len(name) > PlantValidator.MAX_NAME_LENGTH:
            raise PlantValidationError("name", f"Name cannot exceed {PlantValidator.MAX_NAME_LENGTH} characters")

    @staticmethod
    def validate_latin_name(latin_name: str) -> None:
        if not latin_name or not latin_name.strip():
            raise PlantValidationError("latin_name", "Latin name cannot be empty")

        if len(latin_name) < PlantValidator.MIN_LATIN_NAME_LENGTH:
            raise PlantValidationError("latin_name",
                                  f"Latin name must be at least {PlantValidator.MIN_LATIN_NAME_LENGTH} characters")

        if len(latin_name) > PlantValidator.MAX_LATIN_NAME_LENGTH:
            raise PlantValidationError("latin_name",
                                  f"Latin name cannot exceed {PlantValidator.MAX_LATIN_NAME_LENGTH} characters")

    @staticmethod
    def validate_category(category: PlantCategory) -> None:
        if category is None:
            raise PlantValidationError("category", "Category is required")

        if not isinstance(category, PlantCategory):
            raise PlantValidationError("category", "Invalid category type")

        if category == PlantCategory.ALL:
            raise PlantValidationError("category", "Cannot assign 'All' as a plant category")

    @staticmethod
    def validate_location(location: PlantLocation) -> None:
        if location is None:
            raise PlantValidationError("location", "Location is required")

        if not isinstance(location, PlantLocation):
            raise PlantValidationError("location", "Invalid location type")

    @staticmethod
    def validate_date_planted(date_planted: datetime.date) -> None:
        if date_planted is None:
            raise PlantValidationError("date_planted", "Date planted is required")

        if not isinstance(date_planted, datetime.date):
            raise PlantValidationError("date_planted", "Invalid date format")

        if date_planted > datetime.date.today():
            raise PlantValidationError("date_planted", "Cannot plant in the future")

        min_date = datetime.date.today() - datetime.timedelta(days=365 * 500)
        if date_planted < min_date:
            raise PlantValidationError("date_planted", "Date planted is unreasonably old")

    @staticmethod
    def validate_watering_schedule(watering_schedule: int) -> None:
        if watering_schedule is None:
            raise PlantValidationError("watering_schedule", "Watering schedule is required")

        if not isinstance(watering_schedule, int):
            raise PlantValidationError("watering_schedule", "Watering schedule must be an integer")

        if watering_schedule < PlantValidator.MIN_WATERING_DAYS:
            raise PlantValidationError("watering_schedule",
                                  f"Watering schedule must be at least {PlantValidator.MIN_WATERING_DAYS} day")

        if watering_schedule > PlantValidator.MAX_WATERING_DAYS:
            raise PlantValidationError("watering_schedule",
                                  f"Watering schedule cannot exceed {PlantValidator.MAX_WATERING_DAYS} days")

    @staticmethod
    def validate_last_watered(last_watered: datetime.date, date_planted: datetime.date) -> None:
        if last_watered is None:
            raise PlantValidationError("last_watered", "Last watered date is required")

        if not isinstance(last_watered, datetime.date):
            raise PlantValidationError("last_watered", "Invalid date format")

        if last_watered > datetime.date.today():
            raise PlantValidationError("last_watered", "Cannot water in the future")

        if last_watered < date_planted:
            raise PlantValidationError("last_watered", "Cannot water before planting date")

    @staticmethod
    def validate_notes(notes: Optional[str]) -> None:
        """Validate notes field"""
        if notes is not None and len(notes) > PlantValidator.MAX_NOTES_LENGTH:
            raise PlantValidationError("notes", f"Notes cannot exceed {PlantValidator.MAX_NOTES_LENGTH} characters")

    @staticmethod
    def validate_photos(photos: list) -> None:
        """Validate photos list"""
        if photos is not None and len(photos) > PlantValidator.MAX_PHOTOS_PER_PLANT:
            raise PlantValidationError("photos", f"Cannot exceed {PlantValidator.MAX_PHOTOS_PER_PLANT} photos per plant")

    @staticmethod
    def validate_plant_create(
            name: str,
            latin_name: str,
            category: PlantCategory,
            location: PlantLocation,
            date_planted: datetime.date,
            watering_schedule: int
    ) -> None:
        PlantValidator.validate_name(name)
        PlantValidator.validate_latin_name(latin_name)
        PlantValidator.validate_category(category)
        PlantValidator.validate_location(location)
        PlantValidator.validate_date_planted(date_planted)
        PlantValidator.validate_watering_schedule(watering_schedule)

    @staticmethod
    def validate_plant_update(
            name: str,
            latin_name: str,
            category: PlantCategory,
            location: PlantLocation,
            date_planted: datetime.date,
            watering_schedule: int,
            last_watered: datetime.date,
            notes: Optional[str],
            photos: list
    ) -> None:
        PlantValidator.validate_plant_create(name, latin_name, category, location, date_planted, watering_schedule)
        PlantValidator.validate_last_watered(last_watered, date_planted)
        PlantValidator.validate_notes(notes)
        PlantValidator.validate_photos(photos)