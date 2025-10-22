import socket
import time
import json
from src.colors import Colors
from datetime import datetime

class TCPClient:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(f"Connected to CoolNet Control Center at {self.host}:{self.port}")

    def send_actuator_command(self, command_type: str, value: float, location: str = "Server Rack A"):
        """Sender kontrolkommando til aktuatorer"""
        command = {
            "company": "CoolNet IoT",
            "type": "actuator_command",
            "command": command_type,
            "value": value,
            "location": location,
             "timestamp": datetime.now().isoformat()
        }
        
        message = json.dumps(command)
        self.sock.sendall((message + "\n").encode())
        print(f"{Colors.blue}Command sent: {command_type} = {value} at {location}{Colors.reset}")

    def close(self):
        if self.sock:
            self.sock.close()
        print("Disconnected from Control Center.")


if __name__ == "__main__":
    client = TCPClient()
    client.connect()

    # Simuler kontrol af aktuatorer baseret på sensordata
    commands = [
        ("SET_COOLING", 75.0, "Cooling Unit 1"),
        ("SET_PERFORMANCE", 80.0, "Server Rack B"),
        ("ALERT_TECH", 1.0, "Control Room"),
        ("SET_COOLING", 100.0, "Cooling Unit 2")
    ]

    for command, value, location in commands:
        client.send_actuator_command(command, value, location)
        time.sleep(2)

    client.close()