import pytest
from fastapi.testclient import TestClient
from src.http.rest_api_eksempel_3 import app  # <-- ændr evt. hvis din fil ikke hedder main.py

client = TestClient(app)

#@pytest.mark.focus
def test_create_person():
    # Test at oprette en person
    response = client.post(
        "/person",
        data={"person_id": "1337", "navn": "Jens", "alder": 35},
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "gemt"
    assert json_data["data"]["person_id"] == "1337"
    assert json_data["data"]["navn"] == "Jens"
    assert json_data["data"]["alder"] == 35

#@pytest.mark.focus
def test_get_existing_person():
    # Test at hente den samme person (som vi netop oprettede)
    response = client.get("/person/1337")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "ok"
    assert json_data["data"]["person_id"] == "1337"
    assert json_data["data"]["navn"] == "Jens"
    assert json_data["data"]["alder"] == 35

#@pytest.mark.focus
def test_get_non_existing_person():
    # Test at hente en person der ikke findes
    response = client.get("/person/1338")
    assert response.status_code == 200  # app returnerer 200 med fejlstatus i JSON
    json_data = response.json()
    assert json_data["status"] == "fejl"
    assert "findes ikke" in json_data["besked"]

#@pytest.mark.focus
def test_get_person_without_id():
    # Test at kalde /person uden id
    response = client.get("/person")
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["detail"] == "path skal være /person/<person_id>"
