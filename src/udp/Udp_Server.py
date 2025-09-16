# Udp_Server.py
import socket
import threading

class UdpServer:
    def __init__(self):
        self.server_socket = None
        self.is_running = False
        self.recievedMessages = []

    def startServer(self, ip="127.0.0.1", port=9999):
        """Starter UDP serveren"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((ip, port))
        self.is_running = True
        print(f"Server started on {ip}:{port}")

        # Kør serveren i en tråd så den ikke blokerer
        thread = threading.Thread(target=self._receive_loop, daemon=True)
        thread.start()

    def _receive_loop(self):
        """Intern metode der modtager beskeder"""
        while self.is_running:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                message = data.decode("utf-8")
                self.recievedMessages.append(message)
                print(f"Modtaget fra {addr}: {message}")
            except OSError:
                break

    def closeServer(self):
        """Lukker serveren"""
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        print("Server closed")


if __name__ == "__main__":
    server = UdpServer()
    server.startServer()

    try:
        # Holder serveren kørende indtil brugeren stopper programmet
        print("UDP server kører... tryk Ctrl+C for at stoppe")
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopper server...")
        server.closeServer()
