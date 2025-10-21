import pytest
from fastapi.testclient import TestClient
from src.http.rest_api_eksempel_5 import app

client = TestClient(app)

@pytest.mark.focus
# Test POST sensordata og GET aktuel data
def test_post_and_get_current():
    payload = {
        "sensor_id": "sensor1",
        "temperatur": 25.0,
        "luftfugtighed": 40.0,
        "strøm": 120.0
    }
    # POST
    r_post = client.post("/sensor/data", json=payload)
    assert r_post.status_code == 200
    json_post = r_post.json()
    assert json_post["sensor_id"] == "sensor1"
    assert "timestamp" in json_post

    # GET current
    r_get = client.get("/sensor/sensor1/current")
    assert r_get.status_code == 200
    json_get = r_get.json()
    assert json_get["temperatur"] == 25.0

@pytest.mark.focus
# Test historik
def test_history():
    r = client.get("/sensor/sensor1/history")
    assert r.status_code == 200
    json_data = r.json()
    assert len(json_data) >= 1
    assert "temperatur" in json_data[0]

@pytest.mark.focus
# Test config upload og læs
def test_config():
    config_payload = {
        "sensor_id": "sensor1",
        "config": {"interval": "10s", "unit": "C"}
    }
    r_post = client.post("/sensor/config", json=config_payload)
    assert r_post.status_code == 200
    r_get = client.get("/sensor/sensor1/config")
    assert r_get.status_code == 200
    json_data = r_get.json()
    assert json_data["config"]["interval"] == "10s"

@pytest.mark.focus
# Test 404 fejl
def test_404():
    #print("test_404\n")
    r = client.get("/sensor/ukendt/current")
    assert r.status_code == 404
    r = client.get("/sensor/ukendt/history")
    assert r.status_code == 404
    r = client.get("/sensor/ukendt/config")
    assert r.status_code == 404
