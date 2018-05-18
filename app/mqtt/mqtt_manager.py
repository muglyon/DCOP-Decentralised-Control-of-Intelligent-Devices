from helpers.message_types import MessageTypes


class MQTTManager(object):

    CRITICAL_STATE_COEF = 5

    def __init__(self, client, monitored_area=None):
        self.client = client
        self.monitored_area = monitored_area

    def has_no_msg(self):
        return len(self.client.list_msgs_waiting) == 0

    def has_child_msg(self):
        return len(self.client.child_msgs) > 0

    def has_util_msg(self):
        return len(self.client.util_msgs) > 0

    def has_value_msg(self):
        return len(self.client.value_msgs) > 0

    def publish_root_value_msg(self):
        # priority_value = self.monitored_area.get_degree()
        # priority_value += self.CRITICAL_STATE_COEF if self.monitored_area.is_in_critical_state() else 0
        self.client.publish(self.client.ROOT_TOPIC, str(self.monitored_area.id) + ":" + str(self.monitored_area.get_degree()))

    def publish_child_msg_to(self, recipient_id):
        self.client.publish(
            self.client.DCOP_TOPIC + str(recipient_id), MessageTypes.CHILD.value + " " + str(self.monitored_area.id)
        )

    def publish_pseudo_msg_to(self, recipient_id):
        self.client.publish(
            self.client.DCOP_TOPIC + str(recipient_id), MessageTypes.PSEUDO.value + " " + str(self.monitored_area.id)
        )

    def publish_value_msg_to(self, recipient_id, values):
        self.client.publish(
            self.client.DCOP_TOPIC + str(recipient_id), MessageTypes.VALUES.value + " " + values
        )

    def publish_value_msg_to_server(self, values):
        self.client.publish(self.client.SERVER_TOPIC, MessageTypes.VALUES.value + " " + values)

    def publish_util_msg_to(self, recipient_id, data):
        self.client.publish(self.client.DCOP_TOPIC + str(recipient_id), MessageTypes.UTIL.value + " " + data)

    def publish_on_msg_to(self, recipient_id):
        self.client.publish(self.client.DCOP_TOPIC + str(recipient_id), MessageTypes.ON.value)

    def publish_elected_root_msg_to(self, recipient_id, root):
        self.client.publish(self.client.DCOP_TOPIC + str(recipient_id), MessageTypes.ROOT.value + "_" + str(root))
