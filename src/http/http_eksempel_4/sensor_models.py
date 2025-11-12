# sensor_models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    power_consumption: float
    location: str
    timestamp: Optional[str] = None
    company: Optional[str] = "CoolNet IoT"

class SensorConfig(BaseModel):
    sensor_id: str
    sampling_rate: int
    threshold: float
    location: str