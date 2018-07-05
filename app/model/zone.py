from model.monitoring_area import MonitoringArea


class Zone(MonitoringArea):

    def __init__(self, id):
        MonitoringArea.__init__(self, id)
        self.monitored_area_list = []

    def add_room(self, monitored_area):
        self.monitored_area_list.append(monitored_area)

    def to_json_format(self):
        data = {"id": self.id, "rooms": []}

        for room in self.monitored_area_list:
            data["rooms"].append(room.to_json_format())

        return data