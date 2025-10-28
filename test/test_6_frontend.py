import pytest
import httpx
import json
from src.http.http_eksempel_6_frontend.frontend_api import CoolNetFrontend

#@pytest.mark.focus
@pytest.mark.asyncio
async def test_index_page():
    # given
    frontend = CoolNetFrontend()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    # then
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    assert 'CoolNet IoT Dashboard' in response.text  # to verify the title
    assert 'Server Room Monitoring' in response.text  # to verify subtitle
    assert 'Home page' in response.text  # to verify navigation exists
    assert 'Add data' in response.text  # to verify navigation exists

#@pytest.mark.focus
@pytest.mark.asyncio
async def test_add_form_page():
    # given
    frontend = CoolNetFrontend()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/add")

    # then
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    assert 'Add Sensor Data' in response.text  # to verify the title
    assert '<form method="post">' in response.text  # to verify it is a form
    assert 'name="sensor_id"' in response.text  # to verify sensor ID field exists
    assert 'name="temperature"' in response.text  # to verify temperature field exists
    assert 'name="humidity"' in response.text  # to verify humidity field exists
    assert 'name="power_consumption"' in response.text  # to verify power field exists
    assert 'name="location"' in response.text  # to verify location field exists
    assert 'Save Data' in response.text  # to verify submit button exists

#@pytest.mark.focus
@pytest.mark.asyncio
async def test_view_page_no_sensor_id():
    # given
    frontend = CoolNetFrontend()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/view")

    # then - should show error for missing sensor_id
    assert response.status_code == 400
    assert "text/html" in response.headers["content-type"]
    assert 'Angiv sensor ID' in response.text  # to verify error message

#@pytest.mark.focus
@pytest.mark.asyncio
async def test_view_sensor_found(monkeypatch):
    # given mock
    async def mock_get_sensor_by_id(url, *args, **kwargs):
        mock_response = httpx.Response(
            status_code=200,
            content=json.dumps({
                "header": {"status": "ok", "code": 200},
                "body": {
                    "sensor_id": "temp_sensor_01",
                    "temperature": 28.5,
                    "humidity": 45.2,
                    "power_consumption": 15.7,
                    "location": "Server Rack A",
                    "timestamp": "2025-01-22T20:15:47.667123",
                    "company": "CoolNet IoT"
                }
            }),
            headers={"Content-Type": "application/json"}
        )
        return mock_response
    
    monkeypatch.setattr("src.http.http_eksempel_6_frontend.frontend_api.CoolNetFrontend.get_sensor_by_id", mock_get_sensor_by_id)

    # given
    frontend = CoolNetFrontend()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/view?sensor_id=temp_sensor_01")

    # then
    assert response.status_code == 200
    assert "Sensor Details" in response.text  # to verify title exists
    assert "temp_sensor_01" in response.text  # to verify sensor id is shown
    assert "28.5" in response.text  # to verify temperature is shown
    assert "45.2" in response.text  # to verify humidity is shown
    assert "15.7" in response.text  # to verify power consumption is shown
    assert "Server Rack A" in response.text  # to verify location is shown
    assert "Back" in response.text  # to verify back button exists

#@pytest.mark.focus
@pytest.mark.asyncio
async def test_view_sensor_not_found(monkeypatch):
    # given mock
    async def mock_get_sensor_by_id(url, *args, **kwargs):
        mock_response = httpx.Response(
            status_code=404,
            content=json.dumps({"detail": "Sensor 'nonexistent' ikke fundet"}),  
            headers={"Content-Type": "application/json"}
        )
        return mock_response
    
    monkeypatch.setattr("src.http.http_eksempel_6_frontend.frontend_api.CoolNetFrontend.get_sensor_by_id", mock_get_sensor_by_id)

    # given
    frontend = CoolNetFrontend()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/view?sensor_id=nonexistent")

    # then
    assert response.status_code == 404
    assert 'Error' in response.text  # to verify error title exists
    # Brug en mere fleksibel check der håndterer HTML encoding
    assert "Sensor" in response.text and "nonexistent" in response.text and "ikke fundet" in response.text
    assert 'Back' in response.text  # to verify back button exists

#@pytest.mark.focus
@pytest.mark.asyncio
async def test_add_sensor_success(monkeypatch):
    # given mock
    async def mock_post_sensor_data(url, *args, **kwargs):
        mock_response = httpx.Response(
            status_code=200,
            content=json.dumps({
                "header": {"status": "data_received", "code": 200},
                "body": {
                    "sensor_id": "new_sensor",
                    "temperature": 25.0,
                    "humidity": 45.0,
                    "power_consumption": 15.0,
                    "location": "Test Rack",
                    "timestamp": "2025-01-22T10:00:00",
                    "company": "CoolNet IoT"
                }
            }),
            headers={"Content-Type": "application/json"}
        )
        return mock_response
    
    monkeypatch.setattr("src.http.http_eksempel_6_frontend.frontend_api.CoolNetFrontend.post_sensor_data", mock_post_sensor_data)

    # given
    frontend = CoolNetFrontend()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/add", data={
            "sensor_id": "new_sensor",
            "temperature": "25.0",
            "humidity": "45.0",
            "power_consumption": "15.0",
            "location": "Test Rack"
        })

    # then - should redirect to home page on success
    assert response.status_code == 303  # Redirect
    assert response.headers["location"] == "/"

#@pytest.mark.focus
@pytest.mark.asyncio
async def test_backend_error_handling(monkeypatch):
    # given mock - simulate backend error
    async def mock_get_sensors_data(url, *args, **kwargs):
        mock_response = httpx.Response(
            status_code=500,
            content=json.dumps({"detail": "Internal server error"}),
            headers={"Content-Type": "application/json"}
        )
        return mock_response
    
    monkeypatch.setattr("src.http.http_eksempel_6_frontend.frontend_api.CoolNetFrontend.get_sensors_data", mock_get_sensors_data)

    # given
    frontend = CoolNetFrontend()
    app = frontend.app
    transport = httpx.ASGITransport(app=app)

    # when
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    # then - should handle backend error gracefully
    assert response.status_code == 500
    assert "text/html" in response.headers["content-type"]
    assert 'Kunne ikke hente data' in response.text  # to verify error message