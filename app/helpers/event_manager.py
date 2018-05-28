from mqtt.mqtt_manager import MQTTManager


class EventManager(object):

    def __init__(self, monitored_area, mqtt_client):
        self.monitored_area = monitored_area
        self.mqtt_manager = MQTTManager(mqtt_client, monitored_area)

    def notify(self):
        self.mqtt_manager.publish_urgent_msg_to_server(self.monitored_area.id)
