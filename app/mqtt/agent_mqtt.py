from datetime import datetime

from helpers.message_types import MessageTypes
from mqtt.custom_mqtt_class import CustomMQTTClass
from threads.dpop import Dpop


class AgentMQTT(CustomMQTTClass):

    def __init__(self, room):
        CustomMQTTClass.__init__(self, str(room.id) + "/#")

        self.room = room
        self.counter = 0
        self.start_time = datetime.now()

        self.client.list_msgs_waiting = []
        self.client.child_msgs = []
        self.client.util_msgs = []
        self.client.value_msgs = []

    def on_message(self, client, userdata, msg):

        str_msg = str(msg.payload.decode('utf-8'))

        if str_msg == MessageTypes.ON.value:

            print("---------- ITERATION ", self.counter, " --------")

            if self.counter > 0:
                self.room.increment_time(int((datetime.now() - self.start_time).total_seconds() / 60))
                self.room.previous_v = self.room.current_v
                self.start_time = datetime.now()
                print("\n", self.room.to_string())

            thread = Dpop(self.room, client)
            thread.start()
            thread.join(timeout=10)
            self.counter += 1

        elif MessageTypes.CHILD.value in str_msg or MessageTypes.PSEUDO.value in str_msg:
            client.child_msgs.append(str_msg)
        elif MessageTypes.UTIL.value in str_msg:
            client.util_msgs.append(str_msg)
        elif MessageTypes.VALUES.value in str_msg:
            client.value_msgs.append(str_msg)
        else:
            client.list_msgs_waiting.append(str_msg)

        super().on_message(client, userdata, msg)
