import time
import re
import pytest

from src.tcp.Tcp_Server import TCPServer
from src.tcp.Tcp_Client import TCPClient

#@pytest.mark.focus
@pytest.mark.timeout(20)
def test_server_client_message_exchange():
    host, port = "127.0.0.1", 12345
    expected_receive_interval = 1.0
    number_of_messages = 10

    server = TCPServer(host=host, port=port)
    server.start(expected_receive_interval=expected_receive_interval, background=True)

    # Allow server startup
    time.sleep(0.5)

    client = TCPClient(host=host, port=port)
    client.connect()

    for _ in range(number_of_messages):
        timestamp_us = int(time.time() * 1_000_000)
        msg = f"hello world {timestamp_us}"
        client.send_message(msg)
        time.sleep(1)

    client.close()
    server.close()

    # Then it is verified that the server recieved all the messages
    assert(len(server.receivedMessages)==number_of_messages)
