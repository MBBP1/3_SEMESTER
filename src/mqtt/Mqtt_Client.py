import time
import threading
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from src.colors import Colors

class MQTTClient:
    def __init__(self, name="client", device_type="sensor", colorPublish=Colors.green, colorRecieved=Colors.bright_green, broker_host="127.0.0.1", broker_port=1883, client_id=None):
        self.name = name
        self.device_type = device_type  # "sensor", "actuator", "controller"
        self.colorPublish = colorPublish
        self.colorRecieved = colorRecieved 
        
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id=client_id)
        self._connected = False
        self._thread = None
        self.receivedMessages = []
        self.actions_performed = []

        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def connect(self, background=True):
        """Connect to the MQTT broker."""
        self.client.connect(self.broker_host, self.broker_port, keepalive=60)

        if background:
            self._thread = threading.Thread(target=self.client.loop_forever, daemon=True)
            self._thread.start()
        else:
            self.client.loop_start()
            while not self._connected:
                time.sleep(0.1)

        print(f"* {self.name} ({self.device_type}) Connected to broker")
    
    def wait_until_connected(self, timeout=5):
        """Block until connected or timeout"""
        start = time.time()
        while not self._connected:
            if time.time() - start > timeout:
                raise TimeoutError("MQTT client failed to connect in time")
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
        
        # Handle actuator commands
        if self.device_type == "actuator" and msg.topic == "coolnet/actuators/control":
            self._handle_actuator_command(message)

    def _handle_actuator_command(self, message):
        """Handle commands for actuators - kun hvis de er tiltænkt denne enhed"""
        try:
            command = json.loads(message)
            target = command.get("target", "")
            
            # Kun håndter kommandoer der er tiltænkt "All" eller denne specifikke enhed
            if target == "All" or target == self.name:
                if command.get("command") == "SET_COOLING":
                    self.actions_performed.append(f"Cooling set to {command.get('value')}%")
                    print(f"{Colors.cyan}* {self.name}: Cooling adjusted to {command.get('value')}%{Colors.reset}")
                elif command.get("command") == "SET_PERFORMANCE":
                    self.actions_performed.append(f"Performance limited to {command.get('value')}%")
                    print(f"{Colors.cyan}* {self.name}: Performance limited to {command.get('value')}%{Colors.reset}")
                elif command.get("command") == "ALERT_TECH":
                    self.actions_performed.append("Technician alerted")
                    print(f"{Colors.red}* {self.name}: TECHNICIAN ALERTED!{Colors.reset}")
        except:
            pass

    def publish_sensor_data(self, temperature, humidity, power_consumption, location):
        """Publish sensor data from IoT devices"""
        sensor_data = {
            "company": "CoolNet IoT",
            "device_id": self.name,
            "type": "sensor_data",
            "temperature": temperature,
            "humidity": humidity,
            "power_consumption": power_consumption,
            "location": location,
            "timestamp": datetime.now().isoformat()
        }
        self.publish("coolnet/sensors/data", json.dumps(sensor_data))

    def publish_control_command(self, command, value, target_actuator):
        """Publish control commands from controller"""
        control_data = {
            "company": "CoolNet IoT", 
            "type": "control_command",
            "command": command,
            "value": value,
            "target": target_actuator,
            "timestamp": datetime.now().isoformat()
        }
        self.publish("coolnet/actuators/control", json.dumps(control_data))

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
        print(f"* {self.name}: MQTT client closed.")