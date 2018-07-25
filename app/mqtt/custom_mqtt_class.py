import gc
import paho.mqtt.client as mqtt
import constants as c

from logs import log


class CustomMQTTClass:

    def __init__(self, subtopic):

        self.client = mqtt.Client()
        self.client.DCOP_TOPIC = "DCOP/"
        self.client.SERVER_TOPIC = self.client.DCOP_TOPIC + "SERVER/"
        self.client.ROOT_TOPIC = self.client.SERVER_TOPIC + "ROOT"
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.client.list_msgs_waiting = []
        self.client.value_msgs = []

        self.client.avg_msg_size = 0
        self.client.nb_msg_exchanged_total = 0
        self.client.nb_msg_exchanged_current = 0

        self.subtopic = subtopic
        self.topic_to_subscribe = self.client.DCOP_TOPIC + subtopic

    def on_connect(self, client, obj, flags, rc):
        self.client.subscribe(self.topic_to_subscribe)
        log.info("Subscribe", self.subtopic, c.INFO)

    def on_message(self, client, obj, msg):

        data_to_avg = [self.client.avg_msg_size, len(msg.payload)]

        #  todo enlever float
        self.client.avg_msg_size = (sum(data_to_avg)) / float(len(data_to_avg))
        self.client.nb_msg_exchanged_total += 1
        self.client.nb_msg_exchanged_current += 1

        log.info(str(msg.payload.decode('utf-8')), msg.topic, c.INFO)

        gc.collect()

    def on_disconnect(self, client, userdata, rc=0):
        log.info("Disconnected", self.subtopic, c.INFO)
        client.loop_stop()

    def run(self):
        self.client.connect(c.MQTT_SERVER, c.MQTT_PORT, c.KEEP_ALIVE_PERIOD)
        self.client.loop_forever()
