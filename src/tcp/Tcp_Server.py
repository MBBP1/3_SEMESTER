import socket
import threading
from src.colors import Colors

class TCPServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.server_sock = None
        self.conn = None
        self.addr = None
        self._running = False
        
        self.receivedMessages = []
        self.actuator_commands = []

    def start(self, background=True):
        if background:
            thread = threading.Thread(target=self._run, daemon=True)
            thread.start()
        else:
            self._run()

    def _run(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)

        print(f"CoolNet IoT Control Server listening on {self.host}:{self.port}")

        try:
            self.conn, self.addr = self.server_sock.accept()
            print(f"Actuator connected from {self.addr}")
            
            self._running = True
            while self._running:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                
                # Modtag kommandoer til aktuatorer
                print(f"{Colors.green}Command received: {data}{Colors.reset}")
                self.receivedMessages.append(data)
                
                # Simuler eksekvering af kommando
                if "SET_COOLING" in data:
                    self.actuator_commands.append("Cooling system adjusted")
                elif "SET_PERFORMANCE" in data:
                    self.actuator_commands.append("Server performance limited")
                elif "ALERT_TECH" in data:
                    self.actuator_commands.append("Technician alerted")

        except Exception as e:
            print(f"{Colors.red}Server error: {e}{Colors.reset}")
        finally:
            # Tilføj en check så vi ikke lukker to gange
            if self._running:
                self.close()

    def close(self):
        if not self._running:
            return  # Allerede lukket
            
        self._running = False
        if self.conn:
            self.conn.close()
            self.conn = None
        if self.server_sock:
            self.server_sock.close()
            self.server_sock = None
        print("Control Server closed.")