from mqtt.custom_mqtt_class import CustomMQTTClass
from threads.starter import Starter


class ServerMQTT(CustomMQTTClass):

    def __init__(self, hospital):
        CustomMQTTClass.__init__(self, "#")

        self.hospital = hospital

    def on_connect(self, client, obj, flags, rc):
        super().on_connect(client, obj, flags, rc)
        thread = Starter(self.hospital.roomList, client)
        thread.start()

    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)

        if self.client.SERVER_TOPIC in msg.topic:
            client.list_msgs_waiting.append(str(msg.payload.decode('utf-8')))
