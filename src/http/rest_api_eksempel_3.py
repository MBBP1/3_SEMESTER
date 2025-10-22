from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="CoolNet IoT API", description="REST API for CoolNet IoT sensor management")

# "Database" i hukommelsen
sensor_db: dict[str, dict] = {}
sensor_history: list[dict] = []

class SensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    power_consumption: float
    location: str

# POST: Gem sensordata
@app.post("/sensors/data")
def create_sensor_data(
    sensor_id: str = Form(...),
    temperature: float = Form(...),
    humidity: float = Form(...),
    power_consumption: float = Form(...),
    location: str = Form(...)
):
    timestamp = datetime.now().isoformat()
    sensor_data = {
        "sensor_id": sensor_id,
        "temperature": temperature,
        "humidity": humidity,
        "power_consumption": power_consumption,
        "location": location,
        "timestamp": timestamp,
        "company": "CoolNet IoT"
    }
    
    # Gem som aktuel data
    sensor_db[sensor_id] = sensor_data
    # Tilføj til historik
    sensor_history.append(sensor_data)
    
    return {"status": "data_received", "data": sensor_data}

# GET: Hent aktuel sensordata
@app.get("/sensors/data")
def get_all_sensors():
    if not sensor_db:
        return {"status": "error", "message": "No sensor data available"}
    return {"status": "ok", "data": sensor_db}

# GET: Hent specifik sensor
@app.get("/sensors/data/{sensor_id}")
def get_sensor(sensor_id: str):
    if sensor_id not in sensor_db:
        return {"status": "error", "message": f"Sensor '{sensor_id}' not found"}
    return {"status": "ok", "data": sensor_db[sensor_id]}

# GET: Hent historik
@app.get("/sensors/history")
def get_sensor_history():
    if not sensor_history:
        return {"status": "error", "message": "No historical data available"}
    return {"status": "ok", "data": sensor_history}

# GET: Hent historik for specifik sensor
@app.get("/sensors/history/{sensor_id}")
def get_sensor_history_by_id(sensor_id: str):
    sensor_hist = [data for data in sensor_history if data["sensor_id"] == sensor_id]
    if not sensor_hist:
        return {"status": "error", "message": f"No history found for sensor '{sensor_id}'"}
    return {"status": "ok", "data": sensor_hist}

# Fejlhåndtering
@app.get("/sensors")
def get_sensors_without_action():
    raise HTTPException(status_code=400, detail="Path must be /sensors/data or /sensors/data/<sensor_id>")

# HTML form til testing
@app.get("/new-sensor", response_class=HTMLResponse)
def new_sensor_form():
    return """
    <!DOCTYPE html>
    <html lang="da">
    <head>
        <meta charset="UTF-8">
        <title>CoolNet IoT - Add Sensor Data</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 500px; }
            label { display: block; margin-top: 10px; }
            input { width: 100%; padding: 8px; margin: 5px 0; }
            button { background: #0066cc; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>CoolNet IoT - Add Sensor Data</h2>
            <p><i>⚠ Test interface for sensor data submission</i></p>
            <form action="/sensors/data" method="post">
                <label for="sensor_id">Sensor ID:</label>
                <input type="text" id="sensor_id" name="sensor_id" value="sensor_001" required>
                
                <label for="temperature">Temperature (°C):</label>
                <input type="number" id="temperature" name="temperature" step="0.1" value="28.5" required>
                
                <label for="humidity">Humidity (%):</label>
                <input type="number" id="humidity" name="humidity" step="0.1" value="45.2" required>
                
                <label for="power_consumption">Power Consumption (kW):</label>
                <input type="number" id="power_consumption" name="power_consumption" step="0.1" value="15.7" required>
                
                <label for="location">Location:</label>
                <input type="text" id="location" name="location" value="Server Rack A" required>
                
                <button type="submit">Submit Sensor Data</button>
            </form>
        </div>
    </body>
    </html>
    """

# Kør med: uvicorn src.http.rest_api_eksempel_3:app --reload
# Docs: http://127.0.0.1:8000/docs