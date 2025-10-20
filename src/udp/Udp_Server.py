import socket
import threading
from src.colors import Colors

class UDPServer:
    

    def __init__(self):
        # Liste til modtagne beskeder
        self.receivedMessages = []
        self.server_socket = None
        self.is_running = False

    def startServer(self, ip: str, port: int):
        """Starter UDP serveren på den angivne IP og port"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((ip, port))
        self.is_running = True

        print(f"UDP server started on {ip}:{port}")
        
        # Start en tråd til at lytte på beskeder
        thread = threading.Thread(target=self.listen_for_messages)
        thread.daemon = True
        thread.start()

    def listen_for_messages(self):
        """Intern metode til at lytte efter indkommende beskeder"""
        while self.is_running:
            try:
                data, addr = self.server_socket.recvfrom(1024)  # buffer size = 1024 bytes
                message = data.decode("utf-8")
                self.receivedMessages.append(message)
                print(f"{Colors.green}Received from {addr}: {message}{Colors.reset}")
            except Exception as e:
                print(f"{Colors.red}Error receiving message:{Colors.reset}", e)
                self.is_running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        print("UDP server stopped")
    
    def stopServer(self):
        self.is_running = False
        
        

# Eksempel på brug:
if __name__ == "__main__":
    server = UDPServer()
    server.startServer("127.0.0.1", 9999)

    # Holder programmet kørende
    while True:
        pass
