import pytest
import json
from src.http.http_eksempel_4.encryption_utils import decrypt_value
from src.colors import Colors

@pytest.mark.focus
def test_decrypt_sensor_from_file():
    # Load JSON-fil
    with open("db_flat_file.json", "r", encoding="utf-8") as f:
        
        data = json.load(f)

    # Vælg en specifik sensor
    sensor_id = "sensor_100"
    sensor = data["current"].get(sensor_id)
    assert sensor is not None, f"Sensor {sensor_id} ikke fundet!"



    # Print krypterede værdier som de står i filen
    print(f"\n\nEncrypted values from flat file: {(sensor_id)}:")
    print(f"{Colors.red}Location: {sensor["location"]} {Colors.reset}")
    print(f"{Colors.red}Company: {sensor["company"]}{Colors.reset}")

    # Dekrypter felterne
    decrypted_location = decrypt_value(sensor["location"])
    
    decrypted_company = decrypt_value(sensor["company"])
    print("\nDecrypted values:")
    print(f"{Colors.green}Location: {decrypted_location} {Colors.reset}")
    print(f"{Colors.green}Company: {decrypted_company}{Colors.reset}")

