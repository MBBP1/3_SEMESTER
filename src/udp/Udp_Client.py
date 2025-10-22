import socket
import time
import json
import random
from datetime import datetime
from src.colors import Colors

class UDPClient:
    
    def __init__(self, server_ip: str = "127.0.0.1", server_port: int = 9999):
        """Initialiserer klienten med server IP og port"""
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def generate_sensor_data(self):
        """Genererer CoolNet IoT sensordata"""
        return {
            "company": "CoolNet IoT",
            "sensor_id": f"Sensor_{random.randint(100, 999)}",
            "timestamp": datetime.now().isoformat(),
            "temperature": round(random.uniform(18.0, 35.0), 2),
            "humidity": round(random.uniform(30.0, 60.0), 2),
            "power_consumption": round(random.uniform(5.0, 25.0), 2),
            "type": "server_room_monitoring"
        }

    def sendMessage(self, message: str = None, repeat: int = 10, delay_ms: int = 1000):
        """
        Sender en besked til serveren
        :param message: Tekstbeskeden (hvis None, sendes CoolNet sensor data)
        :param repeat: Antal gange beskeden sendes
        :param delay_ms: Forsinkelse i millisekunder mellem hver besked
        """
        for i in range(repeat):
            if message is None:
                # Send CoolNet IoT sensordata
                sensor_data = self.generate_sensor_data()
                msg_to_send = json.dumps(sensor_data)
            else:
                # Send tekstbesked med timestamp (bevarer bagudkompatibilitet)
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S:%f")[:-3]
                msg_to_send = f"{message} {timestamp}"
            
            # Send besked til server
            self.client_socket.sendto(msg_to_send.encode("utf-8"), (self.server_ip, self.server_port))
            
            print(f"{Colors.blue}Sent: {msg_to_send}")

            # Vent delay_ms millisekunder
            time.sleep(delay_ms / 1000.0)


# Kan køres som main
if __name__ == "__main__":
    client = UDPClient()
    
    # Eksempel: Send CoolNet IoT data i stedet for tekst
    print("=== CoolNet IoT Sensor Simulation ===")
    client.sendMessage(repeat=5, delay_ms=1500)  # Sender sensor data