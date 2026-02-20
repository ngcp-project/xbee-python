import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, pan_id: str, mac_address: str, on_rf=None, use_tls: bool = True):
        self.pan_id = str(pan_id)
        self.mac_address = (mac_address or "").upper()
        self.on_rf = on_rf

        self.connected = False
        self._subscriptions: list[tuple[str, int]] = []

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        if use_tls:
            self.client.tls_set()
            self.default_port = 8883
        else:
            self.default_port = 1883

    def _topic_rx(self, dest64: str) -> str:
        return f"xbee/pan/{self.pan_id}/rx/{dest64.upper()}"

    def _topic_broadcast(self) -> str:
        return f"xbee/pan/{self.pan_id}/broadcast"

    def set_username_pw(self, username: str | None = None, password: str | None = None):
        self.client.username_pw_set(username, password)

    def connect(self, host: str, port: int | str | None = None, keepalive: int | str = 60):
        if port is None:
            port = self.default_port
        self.client.connect(host, int(port), int(keepalive))
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe_rf(self, qos: int = 0):
        self._subscribe(self._topic_rx(self.mac_address), qos=qos)
        self._subscribe(self._topic_broadcast(), qos=qos)

    def publish_unicast(self, dest64: str, payload: bytes, *, qos: int = 0, retain: bool = False):
        return self.client.publish(self._topic_rx(dest64), payload, qos=qos, retain=retain)

    def publish_broadcast(self, payload: bytes, *, qos: int = 0, retain: bool = False):
        return self.client.publish(self._topic_broadcast(), payload, qos=qos, retain=retain)

    def _subscribe(self, topic: str, qos: int = 0):
        self._subscriptions.append((topic, qos))
        if self.connected:
            self.client.subscribe(topic, qos=qos)

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        self.connected = (reason_code == 0)
        if self.connected:
            for topic, qos in self._subscriptions:
                client.subscribe(topic, qos=qos)

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self.connected = False

    def _on_message(self, client, userdata, msg):
        if self.on_rf:
            self.on_rf(msg.topic, msg.payload)
