import socket
import time
from datetime import datetime
from src.colors import Colors

class UDPClient:
    
    def __init__(self, server_ip: str = "127.0.0.1", server_port: int = 9999):
        """Initialiserer klienten med server IP og port"""
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendMessage(self, message: str, repeat: int = 10, delay_ms: int = 1000):
        """
        Sender en besked til serveren
        :param message: Tekstbeskeden
        :param repeat: Antal gange beskeden sendes
        :param delay_ms: Forsinkelse i millisekunder mellem hver besked
        """
        for i in range(repeat):
            # Tilføj timestamp i formatet YYYY-MM-DDThh:mm:ss:xxx
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S:%f")[:-3]
            msg_with_time = f"{message} {timestamp}"
            
            # Send besked til server
            self.client_socket.sendto(msg_with_time.encode("utf-8"), (self.server_ip, self.server_port))
            
            print(f"{Colors.yellow}Sent: {msg_with_time}{Colors.reset}")

            # Vent delay_ms millisekunder
            time.sleep(delay_ms / 1000.0)


# Kan køres som main
if __name__ == "__main__":
    client = UDPClient()  # Default 127.0.0.1:9999
    client.sendMessage("hej server")
