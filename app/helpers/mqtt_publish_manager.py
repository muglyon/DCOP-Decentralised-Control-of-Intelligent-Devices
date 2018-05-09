from helpers.message_types import MessageTypes


class MQTTPublishManager(object):

    def __init__(self, mqtt_client, room):
        self.mqtt_client = mqtt_client
        self.room = room

    def publish_root_msg(self):
        self.mqtt_client.publish(self.mqtt_client.ROOT_TOPIC, str(self.room.id) + ":" + str(self.room.get_degree()))

    def publish_child_msg_to(self, recipient_id):
        self.mqtt_client.publish(
            self.mqtt_client.DCOP_TOPIC + str(recipient_id), MessageTypes.CHILD.value + " " + str(self.room.id)
        )

    def publish_pseudo_msg_to(self, recipient_id):
        self.mqtt_client.publish(
            self.mqtt_client.DCOP_TOPIC + str(recipient_id), MessageTypes.PSEUDO.value + " " + str(self.room.id)
        )

    def publish_value_msg_to(self, recipient_id, values):
        self.mqtt_client.publish(
            self.mqtt_client.DCOP_TOPIC + str(recipient_id), MessageTypes.VALUES.value + " " + values
        )

    def publish_value_msg_to_server(self, values):
        self.mqtt_client.publish(self.mqtt_client.SERVER_TOPIC, MessageTypes.VALUES.value + " " + values)

    def publish_util_msg_to(self, recipient_id, data):
        self.mqtt_client.publish(self.mqtt_client.DCOP_TOPIC + str(recipient_id), MessageTypes.UTIL.value + " " + data)
