"""
Integration tests for Plant API endpoints
"""
import datetime
import pytest
from fastapi.testclient import TestClient

from backend.src.main import app
from backend.src.model import PlantCategory, PlantLocation
from backend.src.repository import plant_repository


@pytest.fixture(autouse=True)
def reset_repository():
    """Reset repository before each test"""
    plant_repository._PlantRepository__plants = {}
    plant_repository._PlantRepository__next_id = 1
    plant_repository._PlantRepository__add_mock_plants()
    yield
    # Cleanup after test
    plant_repository._PlantRepository__plants = {}
    plant_repository._PlantRepository__next_id = 1
    plant_repository._PlantRepository__add_mock_plants()


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


class TestPlantAPI:
    """Test suite for Plant API endpoints"""

    # GET /api/plants/ Tests
    def test_get_all_plants_success(self, client):
        """GET all plants should return 200 and list of plants"""
        response = client.get("/api/plants/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Check structure of first plant
        first_plant = data[0]
        assert "id" in first_plant
        assert "name" in first_plant
        assert "latinName" in first_plant  # camelCase
        assert "category" in first_plant
        assert "lastWatered" in first_plant
        assert "age" in first_plant

    # GET /api/plants/{id} Tests
    def test_get_plant_detail_success(self, client):
        """GET plant by ID should return 200 and plant details"""
        # First get all plants to find a valid ID
        all_plants = client.get("/api/plants/").json()
        plant_id = all_plants[0]["id"]

        response = client.get(f"/api/plants/{plant_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == plant_id
        assert "location" in data
        assert "datePlanted" in data
        assert "photoCount" in data
        assert "wateringSchedule" in data
        assert "notes" in data
        assert "photos" in data

    '''
    def test_get_plant_detail_not_found(self, client):
        """GET plant by non-existing ID should return 404"""
        response = client.get("/api/plants/999999")

        assert response.status_code == 404
        assert "detail" in response.json()
    '''

    # POST /api/plants/ Tests
    def test_create_plant_success(self, client):
        """POST valid plant data should return 201 and created plant"""
        new_plant = {
            "name": "New Test Plant",
            "latinName": "Testus newus",
            "category": PlantCategory.TROPICAL.value,
            "location": PlantLocation.WINDOWSILL.value,
            "datePlanted": "2023-01-01",
            "wateringSchedule": 7
        }

        response = client.post("/api/plants/", json=new_plant)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Test Plant"
        assert data["latinName"] == "Testus newus"
        assert data["id"] > 0

    def test_create_plant_invalid_name(self, client):
        """POST plant with empty name should return 400/422"""
        invalid_plant = {
            "name": "",  # Invalid
            "latinName": "Testus newus",
            "category": PlantCategory.TROPICAL.value,
            "location": PlantLocation.WINDOWSILL.value,
            "datePlanted": "2023-01-01",
            "wateringSchedule": 7
        }

        response = client.post("/api/plants/", json=invalid_plant)

        # Should fail validation (either 400 or 422)
        assert response.status_code in [400, 422]

    def test_create_plant_invalid_category(self, client):
        """POST plant with 'ALL' category should return 400/422"""
        invalid_plant = {
            "name": "Test Plant",
            "latinName": "Testus newus",
            "category": PlantCategory.ALL.value,  # Invalid for plants
            "location": PlantLocation.WINDOWSILL.value,
            "datePlanted": "2023-01-01",
            "wateringSchedule": 7
        }

        response = client.post("/api/plants/", json=invalid_plant)

        assert response.status_code in [400, 422]

    def test_create_plant_future_date(self, client):
        """POST plant with future date should return 400/422"""
        future_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        invalid_plant = {
            "name": "Test Plant",
            "latinName": "Testus newus",
            "category": PlantCategory.TROPICAL.value,
            "location": PlantLocation.WINDOWSILL.value,
            "datePlanted": future_date,  # Future date
            "wateringSchedule": 7
        }

        response = client.post("/api/plants/", json=invalid_plant)

        assert response.status_code in [400, 422]

    def test_create_plant_invalid_watering_schedule(self, client):
        """POST plant with invalid watering schedule should return 400/422"""
        invalid_plant = {
            "name": "Test Plant",
            "latinName": "Testus newus",
            "category": PlantCategory.TROPICAL.value,
            "location": PlantLocation.WINDOWSILL.value,
            "datePlanted": "2023-01-01",
            "wateringSchedule": 0  # Invalid
        }

        response = client.post("/api/plants/", json=invalid_plant)

        assert response.status_code in [400, 422]

    def test_create_plant_missing_required_field(self, client):
        """POST plant with missing required field should return 422"""
        invalid_plant = {
            "name": "Test Plant",
            # Missing latinName
            "category": PlantCategory.TROPICAL.value,
            "location": PlantLocation.WINDOWSILL.value,
            "datePlanted": "2023-01-01",
            "wateringSchedule": 7
        }

        response = client.post("/api/plants/", json=invalid_plant)

        assert response.status_code == 422

    # PUT /api/plants/{id} Tests
    def test_update_plant_success(self, client):
        """PUT valid plant data should return 200 and updated plant"""
        # First get a plant ID
        all_plants = client.get("/api/plants/").json()
        plant_id = all_plants[0]["id"]

        update_data = {
            "name": "Updated Plant Name",
            "latinName": "Updatus plantus",
            "category": PlantCategory.BONSAI.value,
            "location": PlantLocation.OUTDOORS.value,
            "datePlanted": "2020-01-01",
            "wateringSchedule": 14,
            "lastWatered": "2020-06-01",
            "notes": "Updated notes",
            "photos": []
        }

        response = client.put(f"/api/plants/{plant_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Plant Name"
        assert data["latinName"] == "Updatus plantus"

    def test_update_plant_not_found(self, client):
        """PUT to non-existing plant should return 404"""
        update_data = {
            "name": "Updated Plant",
            "latinName": "Updatus plantus",
            "category": PlantCategory.TROPICAL.value,
            "location": PlantLocation.INDOORS.value,
            "datePlanted": "2020-01-01",
            "wateringSchedule": 7,
            "lastWatered": "2020-06-01",
            "notes": "",
            "photos": []
        }

        response = client.put("/api/plants/999999", json=update_data)

        assert response.status_code == 404

    def test_update_plant_invalid_last_watered(self, client):
        """PUT with last_watered before date_planted should return 400/422"""
        all_plants = client.get("/api/plants/").json()
        plant_id = all_plants[0]["id"]

        invalid_update = {
            "name": "Updated Plant",
            "latinName": "Updatus plantus",
            "category": PlantCategory.TROPICAL.value,
            "location": PlantLocation.INDOORS.value,
            "datePlanted": "2020-01-01",
            "wateringSchedule": 7,
            "lastWatered": "2019-12-31",  # Before planted
            "notes": "",
            "photos": []
        }

        response = client.put(f"/api/plants/{plant_id}", json=invalid_update)

        assert response.status_code in [400, 422]

    # DELETE /api/plants/{id} Tests
    def test_delete_plant_success(self, client):
        """DELETE existing plant should return 204"""
        # First get a plant ID
        all_plants = client.get("/api/plants/").json()
        initial_count = len(all_plants)
        plant_id = all_plants[0]["id"]

        response = client.delete(f"/api/plants/{plant_id}")

        assert response.status_code == 204

        # Verify deletion
        all_plants_after = client.get("/api/plants/").json()
        assert len(all_plants_after) == initial_count - 1

    def test_delete_plant_non_existing(self, client):
        """DELETE non-existing plant should still return 204"""
        response = client.delete("/api/plants/999999")

        # Most APIs return 204 even if resource doesn't exist for idempotency
        assert response.status_code == 204


class TestStatsAPI:
    """Test suite for Statistics API endpoints"""

    def test_get_statistics_success(self, client):
        """GET statistics should return 200 and stats data"""
        response = client.get("/api/stats/")

        assert response.status_code == 200
        data = response.json()

        assert "totalPlants" in data
        assert "oldestPlant" in data
        assert "totalPhotos" in data
        assert "uniqueLocations" in data
        assert "ageDistribution" in data
        assert "typeDistribution" in data
        assert "photoDistribution" in data
        assert "wateringDistribution" in data
        assert "locationDistribution" in data

        # Check distribution structure
        assert isinstance(data["ageDistribution"], list)
        if len(data["ageDistribution"]) > 0:
            assert "label" in data["ageDistribution"][0]
            assert "count" in data["ageDistribution"][0]

    def test_statistics_reflects_data(self, client):
        """Statistics should reflect actual repository data"""
        # Get current stats
        stats = client.get("/api/stats/").json()
        initial_count = stats["totalPlants"]

        # Create a new plant
        new_plant = {
            "name": "Stats Test Plant",
            "latinName": "Testus stats",
            "category": PlantCategory.SUCCULENT.value,
            "location": PlantLocation.OUTDOORS.value,
            "datePlanted": "2023-01-01",
            "wateringSchedule": 14
        }
        client.post("/api/plants/", json=new_plant)

        # Get updated stats
        updated_stats = client.get("/api/stats/").json()

        assert updated_stats["totalPlants"] == initial_count + 1


class TestRootEndpoint:
    """Test suite for root endpoint"""

    def test_root_endpoint(self, client):
        """GET / should return 200 and welcome message"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data