from mqtt.custom_mqtt_class import CustomMQTTClass
from threads.starter import Starter


class ServerMQTT(CustomMQTTClass):

    def __init__(self, hospital):
        CustomMQTTClass.__init__(self, "DCOP/#")

        self.hospital = hospital
        self.client.listMessages = []

    def on_connect(self, client, obj, flags, rc):
        super().on_connect(client, obj, flags, rc)
        thread = Starter(self.hospital.roomList, client)
        thread.start()

    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)

        if "SERVER" in msg.topic:
            client.listMessages.append(str(msg.payload.decode('utf-8')))
