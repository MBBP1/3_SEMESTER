import socket

import socket
import threading
from src.colors import Colors


class TCPServer:
    def __init__(self, host="127.0.0.1", port=12345, buffer_size=2):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.server_sock = None
        self.conn = None
        self.addr = None
        self._running = False
        self._thread = None

        self.receivedMessages = []
        self.warnings = []
        self.errors =[]

    def start(self, expected_receive_interval=1.0, background=True):
        """Start the TCP server. If background=True, run in a separate thread."""
        if background:
            self._thread = threading.Thread(
                target=self._run, args=(expected_receive_interval,), daemon=True
            )
            self._thread.start()
        else:
            self._run(expected_receive_interval)

    def _run(self, expected_receive_interval):
        """Internal server loop."""
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)

        print(f"TCP server listening on {self.host}:{self.port}")

        try:
            self.conn, self.addr = self.server_sock.accept()
            print(f"Connected by {self.addr}")
            self.conn.settimeout(expected_receive_interval)

            buffer = ""
            print("---")
            self._running = True
            while self._running:
                try:
                    data = self.conn.recv(self.buffer_size).decode()
                    if not data:
                        break
                    buffer += data
                    while "\n" in buffer:
                        msg, buffer = buffer.split("\n", 1)
                        print(f"{Colors.greenColor}Received: {msg}{Colors.resetColor}")
                        self.receivedMessages.append(msg)
                except socket.timeout:
                    warningMsg = "Socket timeout: No message received" 
                    print(f"{Colors.orangeColor}Warning, {warningMsg}{Colors.resetColor}")
                    self.warnings.append(warningMsg)

        except KeyboardInterrupt:
            print("\nServer shutting down...")

        finally:
            self.close()

    def close(self):
        """Close the connection and server socket."""
        self._running = False
        if self.conn:
            self.conn.close()
            self.conn = None
        if self.server_sock:
            self.server_sock.close()
            self.server_sock = None
        print("Server closed.")


if __name__ == "__main__":
    server = TCPServer()
    try:
        # Run in foreground (blocking) when started from terminal
        server.start(expected_receive_interval=1.0, background=False)
    except KeyboardInterrupt:
        print("\nServer interrupted by user.")
    finally:
        server.close()
