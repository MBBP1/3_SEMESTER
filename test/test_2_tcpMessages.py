import time
import pytest
from src.tcp.Tcp_Server import TCPServer
from src.tcp.Tcp_Client import TCPClient

#@pytest.mark.focus
def test_actuator_control_system():
    """Test at CoolNet IoT kan sende kontrolkommandoer til aktuatorer med 100% pålidelighed"""
    
    # given
    host, port = "127.0.0.1", 12345
    number_of_commands = 5

    # when - start kontrolserver
    server = TCPServer(host=host, port=port)
    server.start(background=True)
    time.sleep(0.5)  # Vent på server start

    # Opret og tilslut kontrolklient
    client = TCPClient(host=host, port=port)
    client.connect()

    # Send kontrolkommandoer til aktuatorer
    test_commands = [
        ("SET_COOLING", 80.0, "Main Cooling"),
        ("SET_PERFORMANCE", 75.0, "Server Rack A"), 
        ("ALERT_TECH", 1.0, "Control Room"),
        ("SET_COOLING", 90.0, "Backup Cooling"),
        ("SET_PERFORMANCE", 60.0, "Server Rack B")
    ]

    for command, value, location in test_commands:
        client.send_actuator_command(command, value, location)
        time.sleep(0.5)

    client.close()
    time.sleep(1)  # Vent på sidste beskeder
    server.close()

    # then - verificer at ALLE kommandoer blev modtaget
    sent_count = number_of_commands
    received_count = len(server.receivedMessages)

    print(f"\nAntal sendte beskeder: {sent_count}")
    print(f"Antal modtagne beskeder: {received_count}")

    assert received_count == sent_count