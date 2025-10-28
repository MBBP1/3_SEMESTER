from src.http.http_eksempel_4.coolnet_rest_api import CoolNetRestAPI

# Create API instance with persistence
#api = CoolNetRestAPI(database_file_name="coolnet_sensors.json")
api = CoolNetRestAPI(database_file_name="db_flat_file.json")
app = api.app

# Kør med: uvicorn src.http_eksempel_4.main:app --reload
# Docs: http://127.0.0.1:8000/docs