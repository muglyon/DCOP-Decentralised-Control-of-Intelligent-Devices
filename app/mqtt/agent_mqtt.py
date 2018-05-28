from datetime import datetime
from helpers import log
from helpers.constants import Constants
from helpers.message_types import MessageTypes
from mqtt.custom_mqtt_class import CustomMQTTClass
from threads.dpop import dpop_launch


class AgentMQTT(CustomMQTTClass):

    def __init__(self, monitored_area):
        CustomMQTTClass.__init__(self, str(monitored_area.id) + "/#")

        self.monitored_area = monitored_area
        self.counter = 0
        self.start_time = datetime.now()

        self.client.child_msgs = []
        self.client.util_msgs = []

    def on_message(self, client, obj, msg):

        str_msg = str(msg.payload.decode('utf-8'))

        if MessageTypes.is_on(str_msg):

            log.info("Iteration " + str(self.counter), self.monitored_area.id, Constants.INFO)

            if self.counter > 0:
                self.monitored_area.previous_v = self.monitored_area.current_v
                self.monitored_area.increment_time(int((datetime.now() - self.start_time).total_seconds() / 60))
                self.start_time = datetime.now()

                log.info(self.monitored_area.to_json_format(),
                         self.monitored_area.id,
                         Constants.STATE)

            self.initialize_metrics()
            self.counter += 1

            dpop_launch(self.monitored_area, client)

        elif MessageTypes.CHILD.value in str_msg or MessageTypes.PSEUDO.value in str_msg:
            client.child_msgs.append(str_msg)
        elif MessageTypes.UTIL.value in str_msg:
            client.util_msgs.append(str_msg)
        elif MessageTypes.VALUES.value in str_msg:
            client.value_msgs.append(str_msg)
        else:
            client.list_msgs_waiting.append(str_msg)

        super().on_message(client, obj, msg)

    def initialize_metrics(self):
        self.client.nb_msg_exchanged_current = 0
