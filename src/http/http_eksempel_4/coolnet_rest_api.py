# coolnet_rest_api.py
from fastapi import FastAPI, Form, HTTPException, Request
from datetime import datetime
from src.http.http_eksempel_4.flat_file_loader import FlatFileLoader
from src.http.http_eksempel_4.sensor_models import SensorData, SensorConfig
from src.http.http_eksempel_4.encryption_utils import encrypt_value, decrypt_value

# Importér loggeren fra src.logger
from src.logger.logger import LOGGER as logger

class CoolNetRestAPI:
    def __init__(self, database_file_name: str = "db_flat_file.json"):
        self.flat_file_loader = FlatFileLoader(database_file_name)
        self.sensor_data = {"current": {}, "history": []}
        self.sensor_configs = {}

        self.app = FastAPI(title="CoolNet IoT API", description="REST API with persistence")
        
        # Tilføj middleware for logging af requests
        @self.app.middleware("http")
        async def log_requests(request: Request, call_next):
            response = await call_next(request)
            logger.info("HTTP Request", extra={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "client_ip": request.client.host if request.client else "unknown"
            })
            return response
        
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
        
        # Log endpoints
        self.app.get("/admin/logs")(self.get_logs)
        self.app.delete("/admin/logs")(self.clear_logs)
        
        # Decrypted data endpoint
        self.app.get("/sensors/decrypted")(self.get_decrypted_sensors)

    def on_startup(self):
        """Load data from file when API starts"""
        logger.info("CoolNet IoT API starting - loading data from file")
        data = self.flat_file_loader.load_memory_database_from_file()
        self.sensor_data = data
        logger.info("Data loaded successfully", extra={
            "current_sensors": len(self.sensor_data['current']),
            "historical_records": len(self.sensor_data['history'])
        })

    def create_sensor_data(self, 
                         sensor_id: str = Form(...),
                         temperature: float = Form(...),
                         humidity: float = Form(...),
                         power_consumption: float = Form(...),
                         location: str = Form(...)):
        """Create new sensor data entry"""
        try:
            timestamp = datetime.now().isoformat()
            sensor_entry = {
                "sensor_id": sensor_id,
                "temperature": temperature,
                "humidity": humidity,
                "power_consumption": power_consumption,
                "location": encrypt_value(location),
                "timestamp": timestamp,
                "company": encrypt_value("CoolNet IoT")
            }

            # Update in-memory database
            self.sensor_data["current"][sensor_id] = sensor_entry
            self.sensor_data["history"].append(sensor_entry)

            # Persist to file
            self.flat_file_loader.save_memory_database_to_file(self.sensor_data)

            # Log successful creation
            logger.info("Sensor data created", extra={
                "sensor_id": sensor_id,
                "temperature": temperature,
                "humidity": humidity,
                "location": location
            })

            return {
                "header": {"status": "data_received", "code": 200},
                "body": sensor_entry
            }
            
        except Exception as e:
            logger.error("Failed to create sensor data", extra={
                "sensor_id": sensor_id,
                "error": str(e)
            })
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_all_sensors(self):
        """Get all current sensor data"""
        if not self.sensor_data["current"]:
            logger.warning("No sensor data available")
            raise HTTPException(status_code=404, detail="No sensor data available")
        
        logger.info("Retrieved all sensor data", extra={
            "sensor_count": len(self.sensor_data["current"])
        })
        return {
            "header": {"status": "ok", "code": 200},
            "body": self.sensor_data["current"]
        }

    def get_sensor(self, sensor_id: str):
        """Get specific sensor data"""
        if sensor_id not in self.sensor_data["current"]:
            logger.warning("Sensor not found", extra={"sensor_id": sensor_id})
            raise HTTPException(status_code=404, detail=f"Sensor '{sensor_id}' not found")
        
        logger.info("Retrieved sensor data", extra={"sensor_id": sensor_id})
        return {
            "header": {"status": "ok", "code": 200},
            "body": self.sensor_data["current"][sensor_id]
        }

    def get_sensor_history(self):
        """Get sensor data history"""
        if not self.sensor_data["history"]:
            logger.warning("No historical data available")
            raise HTTPException(status_code=404, detail="No historical data available")
        
        logger.info("Retrieved sensor history", extra={
            "history_count": len(self.sensor_data["history"])
        })
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
        try:
            config_entry = {
                "sensor_id": sensor_id,
                "sampling_rate": sampling_rate,
                "threshold": threshold,
                "location": location
            }
            
            self.sensor_configs[sensor_id] = config_entry
            
            logger.info("Sensor config created", extra={
                "sensor_id": sensor_id,
                "sampling_rate": sampling_rate,
                "threshold": threshold
            })
            
            return {
                "header": {"status": "config_saved", "code": 200},
                "body": config_entry
            }
        except Exception as e:
            logger.error("Failed to create sensor config", extra={
                "sensor_id": sensor_id,
                "error": str(e)
            })
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_sensor_config(self, sensor_id: str):
        """Get sensor configuration"""
        if sensor_id not in self.sensor_configs:
            logger.warning("Sensor config not found", extra={"sensor_id": sensor_id})
            raise HTTPException(status_code=404, detail=f"Configuration for sensor '{sensor_id}' not found")
        
        logger.info("Retrieved sensor config", extra={"sensor_id": sensor_id})
        return {
            "header": {"status": "ok", "code": 200},
            "body": self.sensor_configs[sensor_id]
        }

    def invalid_sensors_endpoint(self):
        """Handle invalid sensors endpoint"""
        logger.warning("Invalid endpoint accessed")
        raise HTTPException(status_code=400, detail="Path must be /sensors/data or /sensors/data/<sensor_id>")
    
    def get_decrypted_sensors(self):
        """Returnér alle sensorer med dekrypteret company/location"""
        try:
            decrypted_data = {}
            for sid, sdata in self.sensor_data["current"].items():
                try:
                    sdata_copy = sdata.copy()
                    sdata_copy["location"] = decrypt_value(sdata["location"])
                    sdata_copy["company"] = decrypt_value(sdata["company"])
                    decrypted_data[sid] = sdata_copy
                except Exception as e:
                    decrypted_data[sid] = {"error": str(e)}
            
            logger.info("Decrypted sensor data retrieved")
            return {
                "header": {"status": "ok", "code": 200},
                "body": decrypted_data
            }
        except Exception as e:
            logger.error("Failed to decrypt sensor data", extra={"error": str(e)})
            raise HTTPException(status_code=500, detail="Decryption error")

    def get_logs(self):
        """Get application logs"""
        try:
            logs = logger.read_file()
            logger.info("Logs retrieved by admin")
            return {
                "header": {"status": "ok", "code": 200},
                "body": {"logs": logs}
            }
        except Exception as e:
            logger.error("Failed to read logs", extra={"error": str(e)})
            raise HTTPException(status_code=500, detail="Failed to read logs")

    def clear_logs(self):
        """Clear application logs"""
        try:
            logger.clean_log()
            logger.info("Logs cleared by admin")
            return {
                "header": {"status": "logs_cleared", "code": 200},
                "body": {"message": "Logs cleared successfully"}
            }
        except Exception as e:
            logger.error("Failed to clear logs", extra={"error": str(e)})
            raise HTTPException(status_code=500, detail="Failed to clear logs")