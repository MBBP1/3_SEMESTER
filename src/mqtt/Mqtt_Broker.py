import asyncio
import threading
from amqtt.broker import Broker
from amqtt.plugins.base import BasePlugin


class MQTTBroker:
    def __init__(self, host="127.0.0.1", port=1883, allow_anonymous=True):
        self.host = host
        self.port = port
        self.allow_anonymous = allow_anonymous
        self._broker = None
        self._loop = None
        self._thread = None
        self._running = False

    def _make_config(self):
        return {
            "listeners": {
                "default": {
                    "type": "tcp",
                    "bind": f"{self.host}:{self.port}",
                }
            },
            "plugins": ["amqtt.plugins.authentication.AnonymousAuthPlugin",],
        }

    async def _start_broker(self):
        self._broker = Broker(self._make_config())
        await self._broker.start()

    def start(self, background=True):
        """Start the MQTT broker. If background=True, runs in a thread."""
        def run():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._running = True
            try:
                self._loop.run_until_complete(self._start_broker())
                self._loop.run_forever()
            except Exception as e:
                print(f"Broker error: {e}")
            finally:
                self._loop.run_until_complete(self._broker.shutdown())

        if background:
            self._thread = threading.Thread(target=run, daemon=True)
            self._thread.start()
        else:
            run()

    def close(self):
        """Stop the broker."""
        if not self._running:
            return
        self._running = False
        if self._loop and self._broker:
            asyncio.run_coroutine_threadsafe(self._broker.shutdown(), self._loop)
            self._loop.call_soon_threadsafe(self._loop.stop)
        print("MQTT broker stopped.")


if __name__ == "__main__":
    broker = MQTTBroker(host="127.0.0.1", port=1883)
    try:
        broker.start(background=False)  # blocking
    except KeyboardInterrupt:
        print("\nBroker interrupted by user.")
    finally:
        broker.close()
