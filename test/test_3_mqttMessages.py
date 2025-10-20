import time
import pytest
from src.colors import Colors

from src.mqtt.Mqtt_Broker import MQTTBroker
from src.mqtt.Mqtt_Client import MQTTClient


@pytest.fixture(scope="module")
def broker():
    b = MQTTBroker(host="127.0.0.1", port=1883)
    b.start(background=True)
    # give the broker time to spin up
    time.sleep(1)
    yield b
    #b.close()


@pytest.fixture
def client_factory():
    clients = []

    def _make_client(client_id):
        colorPublish = Colors.blue
        colorRecieved = Colors.blue
        if(client_id=="C1"):
            colorPublish = Colors.blue
            colorRecieved = Colors.blue
        if(client_id=="C2"):
            colorPublish = Colors.cyan
            colorRecieved = Colors.cyan
        if(client_id=="C3"):
            colorPublish = Colors.magenta
            colorRecieved = Colors.magenta

     
        c = MQTTClient(client_id, colorPublish, colorRecieved, broker_host="127.0.0.1", broker_port=1883, client_id=client_id)
        c.connect(background=True)
        clients.append(c)
        return c

    yield _make_client

    # cleanup
    for c in clients:
        c.close()

#@pytest.mark.focus
def test_pubsub(broker, client_factory):
    # Given
    C1 = client_factory("C1")
    C2 = client_factory("C2")
    C3 = client_factory("C3")

    C1.subscribe("topic 1")
    C2.subscribe("topic 2")
    C3.subscribe("topic 1")

    time.sleep(1)  # allow subscriptions to register

    # When
    numberOfRepeats = 1
    for i in range(numberOfRepeats):
        C1.publish("topic 2", f"C1M{i}")
        C2.publish("topic 1", f"C2M2{i}")
        C3.publish("topic 1", f"C3M3{i}")
        time.sleep(0.1)  # give broker time to route

    # give time for async callbacks to fire
    time.sleep(2)

    # Then
    # C2 must receive 10 messages of C1M...
    c2_msgs = [m for _, m in C2.receivedMessages if m.startswith("C1M")]
    assert len(c2_msgs) == numberOfRepeats

    # C1 must receive 10 messages of C2M...
    c1_msgs_from_c2 = [m for _, m in C1.receivedMessages if m.startswith("C2M2")]
    assert len(c1_msgs_from_c2) == numberOfRepeats

    # C1 must receive 10 messages of C3M...
    c1_msgs_from_c3 = [m for _, m in C1.receivedMessages if m.startswith("C3M3")]
    assert len(c1_msgs_from_c3) ==numberOfRepeats

    # C3 must receive 10 messages of C2M...
    c3_msgs_from_c2 = [m for _, m in C3.receivedMessages if m.startswith("C2M2")]
    assert len(c3_msgs_from_c2) == numberOfRepeats

    # C3 must receive 10 messages of C3M...
    c3_msgs_from_c3 = [m for _, m in C3.receivedMessages if m.startswith("C3M3")]
    assert len(c3_msgs_from_c3) == numberOfRepeats
    
