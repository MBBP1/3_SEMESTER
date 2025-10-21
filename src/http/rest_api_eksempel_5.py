from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

app = FastAPI(title="CoolNet IoT REST API", version="1.0")

# "Database" i hukommelsen
sensor_data: Dict[str, List[Dict]] = {}   # sensor_id -> list af målinger
sensor_configs: Dict[str, Dict] = {}      # sensor_id -> config

# Pydantic-modeller
class SensorDataIn(BaseModel):
    sensor_id: str
    temperatur: float
    luftfugtighed: float
    strøm: float

class SensorDataOut(SensorDataIn):
    timestamp: datetime

class ConfigIn(BaseModel):
    sensor_id: str
    config: Dict[str, str]

class ConfigOut(ConfigIn):
    pass

# -----------------------------
# POST: Send sensordata
# -----------------------------
@app.post("/sensor/data", response_model=SensorDataOut)
def post_sensor_data(data: SensorDataIn):
    entry = data.model_dump()
    entry["timestamp"] = datetime.utcnow()
    sensor_data.setdefault(data.sensor_id, []).append(entry)
    return entry

# -----------------------------
# GET: Hent aktuel data
# -----------------------------
@app.get("/sensor/{sensor_id}/current", response_model=SensorDataOut)
def get_current_data(sensor_id: str):
    if sensor_id not in sensor_data or len(sensor_data[sensor_id]) == 0:
        raise HTTPException(status_code=404, detail="Ingen data for denne sensor")
    # Returner seneste måling
    latest = sorted(sensor_data[sensor_id], key=lambda x: x["timestamp"], reverse=True)[0]
    return latest

# -----------------------------
# GET: Hent historik
# -----------------------------
@app.get("/sensor/{sensor_id}/history", response_model=List[SensorDataOut])
def get_sensor_history(sensor_id: str):
    if sensor_id not in sensor_data or len(sensor_data[sensor_id]) == 0:
        raise HTTPException(status_code=404, detail="Ingen historik for denne sensor")
    return sensor_data[sensor_id]

# -----------------------------
# POST: Upload config
# -----------------------------
@app.post("/sensor/config", response_model=ConfigOut)
def upload_config(config: ConfigIn):
    sensor_configs[config.sensor_id] = config.config
    return config

# -----------------------------
# GET: Læs config
# -----------------------------
@app.get("/sensor/{sensor_id}/config", response_model=ConfigOut)
def get_config(sensor_id: str):
    if sensor_id not in sensor_configs:
        raise HTTPException(status_code=404, detail="Config findes ikke for denne sensor")
    return {"sensor_id": sensor_id, "config": sensor_configs[sensor_id]}