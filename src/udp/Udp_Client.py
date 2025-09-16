# Udp_Client.py
import socket
import time
from datetime import datetime

class UdpClient:
    def __init__(self, server_ip="127.0.0.1", server_port=9999):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendMessage(self, message="hej server", count=10, delay_ms=1000):
        """Sender en besked X antal gange med Y ms mellemrum"""
        for i in range(count):
            # Lav timestamp i format YYYY-MM-DDThh:mm:ss:xxx
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S:%f")[:-3]
            full_message = f"{message} ({timestamp})"

            self.client_socket.sendto(full_message.encode("utf-8"),
            (self.server_ip, self.server_port))
            print(f"Sendt: {full_message}")

            time.sleep(delay_ms / 1000.0)  # konverter ms til sekunder

    def closeClient(self):
        """Lukker klienten"""
        self.client_socket.close()


if __name__ == "__main__":
    # Start client med default værdier
    client = UdpClient()
    client.sendMessage("hej server", count=1, delay_ms=1000)
    
    client.sendMessage(input("Skriv besked: "), count=1, delay_ms=500)
    while input("Vil du sende flere beskeder? (j/n): ").lower() == 'j':
        if input("Vil du sende flere beskeder? (j/n): ").lower() == 'j':
            besked = input("Skriv besked: ")
            count = int (input("Hvor mange gange? "))

            client.sendMessage(besked, count=count)
    client.closeClient()
