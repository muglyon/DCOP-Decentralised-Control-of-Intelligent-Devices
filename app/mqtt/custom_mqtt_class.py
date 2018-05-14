import paho.mqtt.client as mqtt
import logging


class CustomMQTTClass:

    MQTT_SERVER = "10.33.120.194"
    MQTT_PORT = 1883
    KEEP_ALIVE_PERIOD = 60

    def __init__(self, subtopic):

        self.client = mqtt.Client()
        self.client.DCOP_TOPIC = "DCOP/"
        self.client.SERVER_TOPIC = self.client.DCOP_TOPIC + "SERVER/"
        self.client.ROOT_TOPIC = self.client.SERVER_TOPIC + "ROOT"
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.list_msgs_waiting = []

        self.topic_to_subscribe = self.client.DCOP_TOPIC + subtopic

        self.log = logging.getLogger()

    def on_connect(self, client, obj, flags, rc):
        self.client.subscribe(self.topic_to_subscribe)
        self.log.info("Subscribe", extra={'topic': self.topic_to_subscribe})

    def on_message(self, client, obj, msg):
        self.log.info(str(msg.payload.decode('utf-8')), extra={'topic': msg.topic})

    def on_disconnect(self, client, userdata, rc=0):
        self.log.info("Disconnected result code :" + rc, extra={'topic': self.topic_to_subscribe})
        client.loop_stop()

    def run(self):
        self.client.connect(self.MQTT_SERVER, self.MQTT_PORT, self.KEEP_ALIVE_PERIOD)
        self.client.loop_forever()
