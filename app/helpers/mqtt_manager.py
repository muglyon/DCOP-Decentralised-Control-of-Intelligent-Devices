

class MqttManager(object):

    def __init__(self, mqtt_client, room):
        self.mqtt_client = mqtt_client
        self.room = room

    def publish_root_msg(self):
        self.publish_to_topic_msg("DCOP/SERVER/ROOT", str(self.room.id) + ":" + str(self.room.get_degree()))

    def publish_child_msg_to(self, recipient_id):
        self.publish_to_topic_msg("DCOP/" + str(recipient_id), "CHILD " + str(self.room.id))

    def publish_pseudo_msg_to(self, recipient_id):
        self.publish_to_topic_msg("DCOP/" + str(recipient_id), "PSEUDO " + str(self.room.id))

    def publish_value_msg_to(self, recipient_id, values):
        self.publish_to_topic_msg("DCOP/" + str(recipient_id), "VALUES " + values)

    def publish_value_msg_to_server(self, values):
        self.publish_to_topic_msg("DCOP/SERVER/", "VALUES " + values)

    def publish_util_msg_to(self, recipient_id, data):
        self.publish_to_topic_msg("DCOP/" + str(recipient_id), "UTIL " + data)

    def publish_to_topic_msg(self, topic, msg):
        self.mqtt_client.publish(topic, msg)
