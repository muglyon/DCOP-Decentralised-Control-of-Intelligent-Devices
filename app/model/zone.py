from model.monitoring_area import MonitoringArea


class Zone(MonitoringArea):

    def __init__(self, id):
        MonitoringArea.__init__(self, id)
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def attach_observer(self, observer):
        for room in self.rooms:
            room.attach_observer(observer)

    def to_json_format(self):
        data = {"id": self.id, "rooms": []}

        for room in self.rooms:
            data["rooms"].append(room.to_json_format())

        return data
