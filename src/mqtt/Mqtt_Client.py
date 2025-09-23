import time
import threading
import paho.mqtt.client as mqtt
from src.colors import Colors


class MQTTClient:
    def __init__(self, name="client", colorPublish=Colors.green, colorRecieved=Colors.bright_green, broker_host="127.0.0.1", broker_port=1883, client_id=None):
        self.name = name
        self.colorPublish = colorPublish
        self.colorRecieved = colorRecieved 
        
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id=client_id)
        self._connected = False
        self._thread = None
        self.receivedMessages = []

        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def connect(self, background=True):
        """Connect to the MQTT broker."""
        self.client.connect(self.broker_host, self.broker_port, keepalive=60)

        if background:
            # run network loop in separate thread
            self._thread = threading.Thread(target=self.client.loop_forever, daemon=True)
            self._thread.start()
        else:
            # blocking
            self.client.loop_start()
            while not self._connected:
                time.sleep(0.1)

        print(f"* {self.name} Connected to broker {self.broker_host}:{self.broker_port}")
    
    def wait_until_connected(self, timeout=5):
        """Block until connected or timeout"""
        start = time.time()
        while not self._connected:
            if time.time() - start > timeout:
                raise TimeoutError("{MQTT client failed to connect in time")
            time.sleep(0.1)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._connected = True
            print(f"{Colors.green}* {self.name}: MQTT connected successfully{Colors.reset}")
        else:
            print(f"{Colors.red}* {self.name}: MQTT connection failed with code {rc}{Colors.reset}")

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        print(f"{Colors.orange}* {self.name}: MQTT disconnected (rc={rc}){Colors.reset}")

    def _on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"{self.colorRecieved}* {self.name}: Received: {msg.topic} -> {message}{Colors.reset}")
        self.receivedMessages.append((msg.topic, message))

    def publish(self, topic, message):
        """Publish a message to a topic."""
        if not self._connected:
            raise ConnectionError("Client is not connected to a broker.")
        self.client.publish(topic, message)
        print(f"{self.colorPublish}* {self.name}: Published: {topic} -> {message}{Colors.reset}")

    def subscribe(self, topic):
        """Subscribe to a topic to receive messages."""
        if not self._connected:
            raise ConnectionError("Client is not connected to a broker.")
        self.client.subscribe(topic)
        print(f"* {self.name}: Subscribed to topic: {topic}")

    def close(self):
        """Disconnect cleanly."""
        if self._connected:
            self.client.disconnect()
        print("* {self.name}: MQTT client closed.")


if __name__ == "__main__":
    # Example usage
    client = MQTTClient("MQTT_client", Colors.green, Colors.bright_green, broker_host="127.0.0.1", broker_port=1883)
    client.connect(background=True)
    client.wait_until_connected()

    client.subscribe("test/topic")

    for n in range(5):
        timestamp_us = int(time.time() * 1_000_000)
        msg = f"hello world {timestamp_us}"
        client.publish("test/topic", msg)
        time.sleep(1)

    time.sleep(2)  # give some time to receive messages
    client.close()
