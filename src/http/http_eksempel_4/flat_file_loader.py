#flat_file_loader.py
import os
import json
from typing import Dict, Any

class FlatFileLoader:
    def __init__(self, database_file_name: str = "db_flat_file.json"):
        self.database_file_name = database_file_name

    def load_memory_database_from_file(self) -> Dict[str, Any]:
        """Load sensor data from JSON file"""
        in_memory_database = {"current": {}, "history": []}
        try:
            if os.path.exists(self.database_file_name):
                with open(self.database_file_name, "r", encoding="utf-8") as f:
                    in_memory_database = json.load(f)
        except (json.JSONDecodeError, Exception) as e:
            print(f"WARNING: File '{self.database_file_name}' is corrupt or doesn't exist. Creating new database. Error: {e}")
        return in_memory_database

    def save_memory_database_to_file(self, in_memory_database: Dict[str, Any]):
        """Save sensor data to JSON file"""
        with open(self.database_file_name, "w", encoding="utf-8") as f:
            json.dump(in_memory_database, f, indent=2, ensure_ascii=False)