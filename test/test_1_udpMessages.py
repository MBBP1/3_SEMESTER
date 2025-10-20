import pytest, time, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.udp.Udp_Server import UDPServer
from src.udp.Udp_Client import UDPClient


#@pytest.mark.focus
def test_udp_client_server():
    # given
    messages_to_send = 10
    delay_ms = 1000
    expected_min_percentage_recieved = 0.8

    # when
    server = UDPServer()
    server.startServer("127.0.0.1", 9999)
    client = UDPClient("127.0.0.1", 9999)
    client.sendMessage("test besked", repeat=messages_to_send, delay_ms=delay_ms)

    time.sleep(1)
    sent_count = messages_to_send

    server.stopServer()

    # then
    received_count = len(server.receivedMessages)

    print(f"\nAntal sendte beskeder: {sent_count}")
    print(f"Antal modtagne beskeder: {received_count}")

    # Tjek at vi har modtaget mindst X% af beskederne
    assert received_count >= (sent_count * expected_min_percentage_recieved), \
        f"Forventede mindst {expected_min_percentage_recieved}% beskeder, men fik kun {received_count}/{sent_count}"
