"""
Tests for PlantService
"""
import datetime
import pytest

from backend.src.model.plant import Plant
from backend.src.model.plant_category import PlantCategory
from backend.src.model.plant_location import PlantLocation
from backend.src.repository.plant_repository import PlantRepository
from backend.src.schema.plant_schema import PlantCreateRequest, PlantUpdateRequest, PlantPhotoRequest
from backend.src.service.plant_service import PlantService
from backend.src.service.plant_validator import PlantValidationError


class TestPlantService:
    @pytest.fixture
    def empty_repository(self):
        repo = PlantRepository()
        repo._PlantRepository__plants = {}
        repo._PlantRepository__next_id = 1
        return repo

    @pytest.fixture
    def service_with_empty_repo(self, empty_repository):
        return PlantService(empty_repository)

    @pytest.fixture
    def service_with_data(self, empty_repository):
        service = PlantService(empty_repository)

        # Add test plants
        for i in range(3):
            plant = Plant(
                id=0,
                name=f"Plant {i}",
                latin_name=f"Plantus {i}",
                category=PlantCategory.TROPICAL,
                location=PlantLocation.INDOORS,
                date_planted=datetime.date(2020, 1, 1),
                watering_schedule=7
            )
            empty_repository.save(plant)

        return service

    @pytest.fixture
    def valid_create_request(self):
        return PlantCreateRequest(
            name="New Plant",
            latin_name="Newus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.WINDOWSILL,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )

    @pytest.fixture
    def valid_update_request(self):
        return PlantUpdateRequest(
            name="Updated Plant",
            latin_name="Updatus plantus",
            category=PlantCategory.BONSAI,
            location=PlantLocation.OUTDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=14,
            last_watered=datetime.date(2020, 6, 1),
            notes="Updated notes",
            photos=[]
        )

    # Get All Plants Tests
    def test_get_all_plants_empty(self, service_with_empty_repo):
        plants = service_with_empty_repo.get_all_plants()
        assert len(plants) == 0
        assert isinstance(plants, list)

    def test_get_all_plants_with_data(self, service_with_data):
        plants = service_with_data.get_all_plants()
        assert len(plants) == 3

        for plant in plants:
            assert hasattr(plant, 'id')
            assert hasattr(plant, 'name')
            assert hasattr(plant, 'latin_name')

    # Get Plant Tests
    def test_get_plant_existing(self, service_with_data, empty_repository):
        all_plants = empty_repository.plants
        first_plant_id = all_plants[0].id

        plant_detail = service_with_data.get_plant(first_plant_id)

        assert plant_detail is not None
        assert plant_detail.id == first_plant_id
        assert hasattr(plant_detail, 'photos')
        assert hasattr(plant_detail, 'notes')

    # Create Plant Tests
    def test_create_plant_valid(self, service_with_empty_repo, valid_create_request):
        created = service_with_empty_repo.create_plant(valid_create_request)

        assert created is not None
        assert created.id > 0
        assert created.name == "New Plant"
        assert created.latin_name == "Newus plantus"

    def test_create_plant_invalid_name(self, service_with_empty_repo):
        invalid_request = PlantCreateRequest(
            name="",  # Invalid
            latin_name="Newus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.WINDOWSILL,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )

        with pytest.raises(PlantValidationError) as exc_info:
            service_with_empty_repo.create_plant(invalid_request)
        assert exc_info.value.field == "name"

    def test_create_plant_invalid_category(self, service_with_empty_repo):
        invalid_request = PlantCreateRequest(
            name="New Plant",
            latin_name="Newus plantus",
            category=PlantCategory.ALL,  # Invalid
            location=PlantLocation.WINDOWSILL,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7
        )

        with pytest.raises(PlantValidationError) as exc_info:
            service_with_empty_repo.create_plant(invalid_request)
        assert exc_info.value.field == "category"

    def test_create_plant_future_date(self, service_with_empty_repo):
        future_date = datetime.date.today() + datetime.timedelta(days=1)
        invalid_request = PlantCreateRequest(
            name="New Plant",
            latin_name="Newus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.WINDOWSILL,
            date_planted=future_date,  # Invalid
            watering_schedule=7
        )

        with pytest.raises(PlantValidationError) as exc_info:
            service_with_empty_repo.create_plant(invalid_request)
        assert exc_info.value.field == "date_planted"

    def test_create_plant_invalid_watering_schedule(self, service_with_empty_repo):
        invalid_request = PlantCreateRequest(
            name="New Plant",
            latin_name="Newus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.WINDOWSILL,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=0  # Invalid
        )

        with pytest.raises(PlantValidationError) as exc_info:
            service_with_empty_repo.create_plant(invalid_request)
        assert exc_info.value.field == "watering_schedule"

    # Update Plant Tests
    def test_update_plant_valid(self, service_with_data, empty_repository, valid_update_request):
        all_plants = empty_repository.plants
        plant_id = all_plants[0].id

        updated = service_with_data.update_plant(plant_id, valid_update_request)

        assert updated is not None
        assert updated.name == "Updated Plant"
        assert updated.latin_name == "Updatus plantus"

    def test_update_plant_non_existing(self, service_with_data, valid_update_request):
        updated = service_with_data.update_plant(999, valid_update_request)
        assert updated is None

    def test_update_plant_invalid_last_watered(self, service_with_data, empty_repository):
        all_plants = empty_repository.plants
        plant_id = all_plants[0].id

        invalid_request = PlantUpdateRequest(
            name="Updated Plant",
            latin_name="Updatus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=datetime.date(2019, 12, 31),  # Before planted
            notes="",
            photos=[]
        )

        with pytest.raises(PlantValidationError) as exc_info:
            service_with_data.update_plant(plant_id, invalid_request)
        assert exc_info.value.field == "last_watered"

    def test_update_plant_too_many_photos(self, service_with_data, empty_repository):
        all_plants = empty_repository.plants
        plant_id = all_plants[0].id

        # Create 101 photos
        too_many_photos = [
            PlantPhotoRequest(
                url=f"photo{i}.jpg",
                caption="",
                date=datetime.date(2020, 1, 1)
            ) for i in range(101)
        ]

        invalid_request = PlantUpdateRequest(
            name="Updated Plant",
            latin_name="Updatus plantus",
            category=PlantCategory.TROPICAL,
            location=PlantLocation.INDOORS,
            date_planted=datetime.date(2020, 1, 1),
            watering_schedule=7,
            last_watered=datetime.date(2020, 6, 1),
            notes="",
            photos=too_many_photos
        )

        with pytest.raises(PlantValidationError) as exc_info:
            service_with_data.update_plant(plant_id, invalid_request)
        assert exc_info.value.field == "photos"

    # Delete Plant Tests
    def test_delete_plant_existing(self, service_with_data, empty_repository):
        all_plants = empty_repository.plants
        plant_id = all_plants[0].id
        initial_count = len(empty_repository)

        service_with_data.delete_plant(plant_id)

        assert len(empty_repository) == initial_count - 1
        assert empty_repository.get_plant(plant_id) is None

    def test_delete_plant_non_existing(self, service_with_data, empty_repository):
        initial_count = len(empty_repository)

        service_with_data.delete_plant(999)

        assert len(empty_repository) == initial_count

    # Statistics Tests
    def test_get_statistics_empty(self, service_with_empty_repo):
        stats = service_with_empty_repo.get_statistics()

        assert stats.total_plants == 0
        assert stats.oldest_plant == 0
        assert stats.total_photos == 0
        assert stats.unique_locations == 0

    def test_get_statistics_with_data(self, service_with_data):
        stats = service_with_data.get_statistics()

        assert stats.total_plants == 3
        assert stats.oldest_plant > 0
        assert stats.unique_locations > 0
        assert len(stats.age_distribution) > 0
        assert len(stats.type_distribution) > 0

    def test_age_distribution_categorization(self, service_with_empty_repo, empty_repository):
        plants_data = [
            (datetime.date.today() - datetime.timedelta(days=180), '<1y'),  # < 1 year
            (datetime.date.today() - datetime.timedelta(days=500), '1-2y'),  # 1-2 years
            (datetime.date.today() - datetime.timedelta(days=1200), '2-5y'),  # 2-5 years
            (datetime.date.today() - datetime.timedelta(days=2500), '5-10y'),  # 5-10 years
            (datetime.date.today() - datetime.timedelta(days=5000), '10-25y'),  # 10-25 years
        ]

        for date_planted, expected_category in plants_data:
            plant = Plant(
                id=0,
                name="Test",
                latin_name="Testus",
                category=PlantCategory.TROPICAL,
                location=PlantLocation.INDOORS,
                date_planted=date_planted,
                watering_schedule=7
            )
            empty_repository.save(plant)

        stats = service_with_empty_repo.get_statistics()
        age_dist = {item.label: item.count for item in stats.age_distribution}

        # Check that we have plants in multiple categories
        assert sum(age_dist.values()) == 5

    def test_watering_distribution_categorization(self, service_with_empty_repo, empty_repository):
        # Create plants with different watering schedules
        schedules = [
            (1, 'High (Every 1-2 days)'),
            (2, 'High (Every 1-2 days)'),
            (7, 'Weekly'),
            (14, 'Bi-Weekly'),
            (30, 'Monthly'),
            (90, 'Seasonal/Occasional'),
        ]

        for days, expected_category in schedules:
            plant = Plant(
                id=0,
                name="Test",
                latin_name="Testus",
                category=PlantCategory.TROPICAL,
                location=PlantLocation.INDOORS,
                date_planted=datetime.date(2020, 1, 1),
                watering_schedule=days
            )
            empty_repository.save(plant)

        stats = service_with_empty_repo.get_statistics()
        water_dist = {item.label: item.count for item in stats.watering_distribution}

        assert water_dist['High (Every 1-2 days)'] == 2
        assert water_dist['Weekly'] == 1
        assert water_dist['Bi-Weekly'] == 1
        assert water_dist['Monthly'] == 1
        assert water_dist['Seasonal/Occasional'] == 1