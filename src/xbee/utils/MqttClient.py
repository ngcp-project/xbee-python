# import paho.mqtt.client as mqtt

# class MqttClient():

#     def __init__(self, pan_id: str, mac_address):
#         self.pan_id = pan_id
#         self.mac_address = mac_address

#         self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.tls_set()

#     # Topic Helpers

#     def _topic_rx(self, dest_address: str) -> str:
#         return f"xbee/pan/{self.pan_id}/rx/{dest_address.upper()}"

#     def _topic_broadcast(self) -> str:
#         return f"xbee/pan/{self.pan_id}/broadcast"

#     def _topic_tx(self) -> str:
#         return f"xbee/pan/{self.pan_id}/tx"



#     def set_username_pw(self, username: str | None = None, password: str | None = None):
#         self.client.username_pw_set(username, password)

#     def connect(self, host: str, port: int = 8883, keepalive: int = 60):
#         try:
#             self.client.connect(host, port, keepalive)
#             self.client.loop_start()
#         # except socket.gaierror as e:
#         #     raise ConnectionError(f"DNS resolution failed for host '{host}': {e}") from e
#         # except ssl.SSLError as e:
#         #     raise ConnectionError(f"TLS/SSL error while connecting to '{host}:{port}': {e}") from e
#         except Exception as e:
#             raise ConnectionError(f"MQTT connection failed: {e}") from e

#     def disconnect(self) -> None:
#         self.client.loop_stop()
#         self.client.disconnect()

#     # The callback for when the client receives a CONNACK response from the server.
#     def on_connect(self, client, userdata, flags, reason_code, properties):
#         print(f"MQTT: Connected with result code {reason_code}")
#         # Subscribing in on_connect() means that if we lose the connection and
#         # reconnect then subscriptions will be renewed.

#     # The callback for when a PUBLISH message is received from the server.
#     def on_message(self, client, userdata, msg):
#         print(msg.topic+" "+str(msg.payload))


#     def subscribe_rf(self, qos: int = 0) -> None:
#         """
#         Subscribe this node to:
#           - unicast RX for mac_address
#           - broadcast for PAN
#         """
#         self._subscribe(self._topic_rx(self.mac_address), qos=qos)
#         self._subscribe(self._topic_broadcast(), qos=qos)

#     def publish_unicast(
#         self,
#         dest_address: str,
#         payload: str,
#         *,
#         qos: int = 0,
#         retain: bool = False,
#     ):
#         """
#         Publish an RF-like packet to a specific destination.
#         In router_mode=True: publish to .../tx and include dest_address in payload.
#         In router_mode=False: publish directly to .../rx/<dest_address>.
#         """

#         topic = self._topic_tx() if self.router_mode else self._topic_rx(dest_address)
#         return self.client.publish(topic, payload, qos=qos, retain=retain)

#     def publish_broadcast(
#         self,
#         payload: str,
#         *,
#         qos: int = 0,
#         retain: bool = False,
#         rssi: int | None = None,
#         lqi: int | None = None,
#     ):
#         """
#         Broadcast to the whole PAN.
#         In router_mode=True: publish to .../tx and set broadcast True.
#         In router_mode=False: publish directly to .../broadcast.
#         """

#         topic = self._topic_tx() if self.router_mode else self._topic_broadcast()
#         return self.client.publish(topic, payload, qos=qos, retain=retain)



#     # Should be able to broadcast or send to specific topic (vehicle)
#     def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
#         return self.client.publish(topic, payload, qos=qos, retain=retain)


#     def subscribe(self, topic: str, qos: int = 0):
#         self.client.subscribe(topic)

#     def _subscribe(self, topic: str, qos: int = 0) -> None:
#         self._subscriptions.append((topic, qos))
#         if self.connected:
#             self.client.subscribe(topic, qos=qos)

import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, pan_id: str, mac_address: str, on_rf=None):
        self.pan_id = str(pan_id)
        self.mac_address = (mac_address or "").upper()
        self.on_rf = on_rf

        self.connected = False
        self._subscriptions = []

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        self.client.tls_set()  # EMQX cloud typically uses TLS

    # Topic helpers
    def _topic_rx(self, dest_address: str) -> str:
        return f"xbee/pan/{self.pan_id}/rx/{dest_address.upper()}"

    def _topic_broadcast(self) -> str:
        return f"xbee/pan/{self.pan_id}/broadcast"

    def set_username_pw(self, username: str | None = None, password: str | None = None):
        self.client.username_pw_set(username, password)

    def connect(self, host: str, port: int = 8883, keepalive: int = 60):
        port = int(port)  # defensive; avoids your earlier str-port crash
        self.client.connect(host, port, keepalive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe_rf(self, qos: int = 0):
        self._subscribe(self._topic_rx(self.mac_address), qos=qos)
        self._subscribe(self._topic_broadcast(), qos=qos)

    def publish_unicast(self, dest_address: str, payload: str, *, qos: int = 0, retain: bool = False):
        topic = self._topic_rx(dest_address)
        return self.client.publish(topic, payload, qos=qos, retain=retain)

    def publish_broadcast(self, payload: str, *, qos: int = 0, retain: bool = False):
        topic = self._topic_broadcast()
        return self.client.publish(topic, payload, qos=qos, retain=retain)

    def _subscribe(self, topic: str, qos: int = 0):
        self._subscriptions.append((topic, qos))
        if self.connected:
            self.client.subscribe(topic, qos=qos)

    # Callbacks
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        self.connected = (reason_code == 0)
        print(f"MQTT: Connected reason_code={reason_code}")

        if self.connected:
            for topic, qos in self._subscriptions:
                client.subscribe(topic, qos=qos)

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self.connected = False
        print(f"MQTT: Disconnected reason_code={reason_code}")

    def _on_message(self, client, userdata, msg):
        raw = msg.payload.decode("utf-8", errors="replace")
        if self.on_rf:
            self.on_rf({"topic": msg.topic, "raw_payload": raw})
        else:
            print(msg.topic, raw)
