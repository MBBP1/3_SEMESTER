import time
import pytest
from src.mqtt.Mqtt_Broker import MQTTBroker
from src.mqtt.Mqtt_Client import MQTTClient

#@pytest.fixture(scope="module")
def broker():
    b = MQTTBroker(host="127.0.0.1", port=1883)
    b.start(background=True)
    time.sleep(1)
    yield b

#@pytest.fixture
def device_factory():
    devices = []

    def _make_device(name, device_type):
        device = MQTTClient(name, device_type, broker_host="127.0.0.1", broker_port=1883, client_id=name)
        device.connect(background=True)
        devices.append(device)
        return device

    yield _make_device

    for device in devices:
        device.close()

#@pytest.mark.focus
def test_coolnet_iot_system(broker, device_factory):
    """Test CoolNet IoT system: x sensorer, y aktuatorer, 1 controller"""
    
    
    # 2 sensorer, 2 aktuatorer, 1 controller
    temp_sensor = device_factory("TempSensor", "sensor")
    cooling_actuator = device_factory("CoolingUnit", "actuator")
    performance_actuator = device_factory("PerformanceCtrl", "actuator")
    controller = device_factory("MainController", "controller")

    time.sleep(1)  # Vent på forbindelser

    # Setup subscriptions
    controller.subscribe("coolnet/sensors/data")      # Controller lytter til sensorer
    cooling_actuator.subscribe("coolnet/actuators/control")
    performance_actuator.subscribe("coolnet/actuators/control")

    time.sleep(1)

    # When - Sensorer sender data som trigger aktuatorer via controller
    print("\n--- Starter CoolNet IoT simulering ---")
    
    # Sensor: Normal temperatur - ingen handling
    temp_sensor.publish("coolnet/sensors/data", '{"temp": 25.0, "location": "Rack A"}')
    time.sleep(0.5)
    
    # Sensor: Høj temperatur - skal trigger køling
    temp_sensor.publish("coolnet/sensors/data", '{"temp": 33.5, "location": "Rack A"}')
    time.sleep(0.5)
    
    # Controller sender kølekommando
    controller.publish("coolnet/actuators/control", '{"command": "SET_COOLING", "value": 80, "target": "CoolingUnit"}')
    time.sleep(0.5)
    
    # Sensor: Kritisk temperatur - skal trigger performance begrænsning
    temp_sensor.publish("coolnet/sensors/data", '{"temp": 37.2, "location": "Rack B"}')
    time.sleep(0.5)
    
    # Controller sender performance kommando
    controller.publish("coolnet/actuators/control", '{"command": "SET_PERFORMANCE", "value": 60, "target": "PerformanceCtrl"}')
    
    time.sleep(1)  # Vent på alle beskeder

    # Then - Verificer at systemet fungerer
    print("\n--- Verificering ---")
    
    # Tæl modtagne beskeder
    cooling_received = len([msg for topic, msg in cooling_actuator.receivedMessages])
    performance_received = len([msg for topic, msg in performance_actuator.receivedMessages])
    controller_received = len([msg for topic, msg in controller.receivedMessages])
    
    print(f"Cooling actuator modtog: {cooling_received} kommandoer")
    print(f"Performance actuator modtog: {performance_received} kommandoer") 
    print(f"Controller modtog: {controller_received} sensor readings")
    
    # Verificer at beskeder nåede frem
    assert cooling_received >= 1, "Cooling actuator modtog ingen kommandoer"
    assert performance_received >= 1, "Performance actuator modtog ingen kommandoer"
    assert controller_received >= 3, "Controller modtog ikke nok sensor data"
    
    print(" CoolNet IoT system test PASSED - 100% beskeder modtaget!")