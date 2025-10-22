from fastapi import FastAPI, Form, HTTPException
from datetime import datetime
from src.http.http_eksempel_4.flat_file_loader import FlatFileLoader
from src.http.http_eksempel_4.sensor_models import SensorData, SensorConfig

class CoolNetRestAPI:
    def __init__(self, database_file_name: str = "coolnet_sensors.json"):
        self.flat_file_loader = FlatFileLoader(database_file_name)
        self.sensor_data = {"current": {}, "history": []}
        self.sensor_configs = {}

        self.app = FastAPI(title="CoolNet IoT API", description="REST API with persistence")
        self.app.add_event_handler("startup", self.on_startup)

        # Register endpoints
        self.app.post("/sensors/data")(self.create_sensor_data)
        self.app.get("/sensors/data")(self.get_all_sensors)
        self.app.get("/sensors/data/{sensor_id}")(self.get_sensor)
        self.app.get("/sensors/history")(self.get_sensor_history)
        self.app.get("/sensors")(self.invalid_sensors_endpoint)
        
        # Config endpoints
        self.app.post("/sensors/config")(self.create_sensor_config)
        self.app.get("/sensors/config/{sensor_id}")(self.get_sensor_config)

    def on_startup(self):
        """Load data from file when API starts"""
        print("CoolNet IoT API starting - loading data from file...")
        data = self.flat_file_loader.load_memory_database_from_file()
        self.sensor_data = data
        print(f"Loaded {len(self.sensor_data['current'])} current sensor readings")
        print(f"Loaded {len(self.sensor_data['history'])} historical records")

    def create_sensor_data(self, 
                         sensor_id: str = Form(...),
                         temperature: float = Form(...),
                         humidity: float = Form(...),
                         power_consumption: float = Form(...),
                         location: str = Form(...)):
        """Create new sensor data entry"""
        timestamp = datetime.now().isoformat()
        sensor_entry = {
            "sensor_id": sensor_id,
            "temperature": temperature,
            "humidity": humidity,
            "power_consumption": power_consumption,
            "location": location,
            "timestamp": timestamp,
            "company": "CoolNet IoT"
        }

        # Update in-memory database
        self.sensor_data["current"][sensor_id] = sensor_entry
        self.sensor_data["history"].append(sensor_entry)

        # Persist to file
        self.flat_file_loader.save_memory_database_to_file(self.sensor_data)

        return {
            "header": {"status": "data_received", "code": 200},
            "body": sensor_entry
        }

    def get_all_sensors(self):
        """Get all current sensor data"""
        if not self.sensor_data["current"]:
            raise HTTPException(status_code=404, detail="No sensor data available")
        return {
            "header": {"status": "ok", "code": 200},
            "body": self.sensor_data["current"]
        }

    def get_sensor(self, sensor_id: str):
        """Get specific sensor data"""
        if sensor_id not in self.sensor_data["current"]:
            raise HTTPException(status_code=404, detail=f"Sensor '{sensor_id}' not found")
        return {
            "header": {"status": "ok", "code": 200},
            "body": self.sensor_data["current"][sensor_id]
        }

    def get_sensor_history(self):
        """Get sensor data history"""
        if not self.sensor_data["history"]:
            raise HTTPException(status_code=404, detail="No historical data available")
        return {
            "header": {"status": "ok", "code": 200},
            "body": self.sensor_data["history"]
        }

    def create_sensor_config(self,
                           sensor_id: str = Form(...),
                           sampling_rate: int = Form(...),
                           threshold: float = Form(...),
                           location: str = Form(...)):
        """Create sensor configuration"""
        config_entry = {
            "sensor_id": sensor_id,
            "sampling_rate": sampling_rate,
            "threshold": threshold,
            "location": location
        }
        
        self.sensor_configs[sensor_id] = config_entry
        return {
            "header": {"status": "config_saved", "code": 200},
            "body": config_entry
        }

    def get_sensor_config(self, sensor_id: str):
        """Get sensor configuration"""
        if sensor_id not in self.sensor_configs:
            raise HTTPException(status_code=404, detail=f"Configuration for sensor '{sensor_id}' not found")
        return {
            "header": {"status": "ok", "code": 200},
            "body": self.sensor_configs[sensor_id]
        }

    def invalid_sensors_endpoint(self):
        """Handle invalid sensors endpoint"""
        raise HTTPException(status_code=400, detail="Path must be /sensors/data or /sensors/data/<sensor_id>")