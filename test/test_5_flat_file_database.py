import json
import os
import pytest
from fastapi.testclient import TestClient
from src.http.http_eksempel_4.coolnet_rest_api import CoolNetRestAPI

# Helpers
def create_json_file(filename: str, content: dict):
    """Helper to create test JSON files"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

def delete_json_files():
    """Clean up test files"""
    filename = "coolnet_sensors_test.json"
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def cleanup_files(scope="function", autouse=True):
    """Clean up before and after each test"""
    delete_json_files()
    yield
    delete_json_files()

# Tests
#@pytest.mark.focus
def test_start_api_with_empty_file_CRUD_Read(cleanup_files):
    """Test starting API with empty database file"""
    # Given
    create_json_file("coolnet_sensors_test.json", {"current": {}, "history": []})

    # When
    api = CoolNetRestAPI("coolnet_sensors_test.json")
    client = TestClient(api.app)
    api.on_startup()

    # Then
    response = client.get("/sensors/data/non_existent_sensor")
    assert response.status_code == 404

#@pytest.mark.focus
def test_start_api_with_existing_data_CRUD_Read(cleanup_files):
    """Test starting API with existing sensor data"""
    # Given
    filename = "coolnet_sensors_test.json"
    existing_data = {
        "current": {
            "temp_sensor_01": {
                "sensor_id": "temp_sensor_01",
                "temperature": 28.5,
                "humidity": 45.2,
                "power_consumption": 15.7,
                "location": "Server Rack A",
                "timestamp": "2025-01-22T20:15:47.667123",
                "company": "CoolNet IoT"
            }
        },
        "history": [
            {
                "sensor_id": "temp_sensor_01",
                "temperature": 28.5,
                "humidity": 45.2,
                "power_consumption": 15.7,
                "location": "Server Rack A",
                "timestamp": "2025-01-22T20:15:47.667123",
                "company": "CoolNet IoT"
            }
        ]
    }
    create_json_file(filename, existing_data)

    # When
    api = CoolNetRestAPI(filename)
    client = TestClient(api.app)
    api.on_startup()

    # Then
    response = client.get("/sensors/data/temp_sensor_01")
    assert response.status_code == 200
    data = response.json()
    assert data["body"]["temperature"] == 28.5
    assert data["body"]["location"] == "Server Rack A"

#@pytest.mark.focus
def test_create_sensor_persists_to_file_CRUD_Create(cleanup_files):
    """Test that creating sensor data persists to file"""
    # Given
    filename = "coolnet_sensors_test.json"
    api = CoolNetRestAPI(filename)
    client = TestClient(api.app)
    api.on_startup()

    # When
    response = client.post(
        "/sensors/data",
        data={
            "sensor_id": "new_sensor_01",
            "temperature": 25.5,
            "humidity": 50.0,
            "power_consumption": 12.3,
            "location": "Test Rack"
        }
    )
    assert response.status_code == 200
    assert os.path.exists(filename)

    # Then - Verify file content
    with open(filename, "r", encoding="utf-8") as f:
        file_data = json.load(f)
    assert "new_sensor_01" in file_data["current"]
    assert len(file_data["history"]) == 1

#@pytest.mark.focus
def test_persistence_between_sessions_CRUD_Create_restart_Read(cleanup_files):
    """Test data persistence between API restarts"""
    # Given - First session
    filename = "coolnet_sensors_test.json"
    api1 = CoolNetRestAPI(filename)
    client1 = TestClient(api1.app)
    api1.on_startup()
    
    # Create data in first session
    client1.post(
        "/sensors/data",
        data={
            "sensor_id": "persistent_sensor",
            "temperature": 30.0,
            "humidity": 40.0,
            "power_consumption": 18.5,
            "location": "Persistent Rack"
        }
    )

    # When - Second session (simulating restart)
    api2 = CoolNetRestAPI(filename)
    client2 = TestClient(api2.app)
    api2.on_startup()

    # Then - Data should be available in second session
    response = client2.get("/sensors/data/persistent_sensor")
    assert response.status_code == 200
    assert response.json()["body"]["sensor_id"] == "persistent_sensor"
    assert response.json()["body"]["temperature"] == 30.0

#@pytest.mark.focus
def test_sensor_config_operations(cleanup_files):
    """Test sensor configuration CRUD operations"""
    # Given
    api = CoolNetRestAPI("coolnet_sensors_test.json")
    client = TestClient(api.app)
    api.on_startup()

    # When - Create config
    response = client.post(
        "/sensors/config",
        data={
            "sensor_id": "config_sensor_01",
            "sampling_rate": 5,
            "threshold": 30.0,
            "location": "Config Rack"
        }
    )
    assert response.status_code == 200

    # Then - Read config
    response = client.get("/sensors/config/config_sensor_01")
    assert response.status_code == 200
    assert response.json()["body"]["sampling_rate"] == 5