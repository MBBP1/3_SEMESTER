import pytest
from fastapi.testclient import TestClient
from src.http.rest_api_eksempel_3 import app

client = TestClient(app)

#@pytest.mark.focus
def test_create_sensor_data():
    """Test at oprette sensordata"""
    response = client.post(
        "/sensors/data",
        data={
            "sensor_id": "temp_sensor_01",
            "temperature": 28.5,
            "humidity": 45.2,
            "power_consumption": 15.7,
            "location": "Server Rack A"
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "data_received"
    assert json_data["data"]["sensor_id"] == "temp_sensor_01"
    assert json_data["data"]["temperature"] == 28.5
    assert json_data["data"]["company"] == "CoolNet IoT"

#@pytest.mark.focus
def test_get_existing_sensor():
    """Test at hente eksisterende sensor"""
    response = client.get("/sensors/data/temp_sensor_01")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert json_data["data"]["sensor_id"] == "temp_sensor_01"
    assert json_data["data"]["location"] == "Server Rack A"

#@pytest.mark.focus
def test_get_non_existing_sensor():
    """Test at hente sensor der ikke findes"""
    response = client.get("/sensors/data/non_existent_sensor")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "error"
    assert "not found" in json_data["message"]

#@pytest.mark.focus
def test_get_all_sensors():
    """Test at hente alle sensorer"""
    response = client.get("/sensors/data")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data

#@pytest.mark.focus
def test_get_sensor_history():
    """Test at hente historik"""
    response = client.get("/sensors/history")
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data

#@pytest.mark.focus
def test_get_sensors_without_action():
    """Test ugyldig endpoint - skal give 400"""
    response = client.get("/sensors")
    assert response.status_code == 400
    json_data = response.json()
    assert "detail" in json_data