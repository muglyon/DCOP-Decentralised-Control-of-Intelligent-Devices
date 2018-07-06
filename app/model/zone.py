from model.monitoring_area import MonitoringArea
from constants import Constants


class Zone(MonitoringArea):

    def __init__(self, id):
        MonitoringArea.__init__(self, id)
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def get_room_who_need_intervention(self):
        r = []
        for room in self.rooms:
            if room.is_tau_too_high() \
                    or room.is_in_critical_state() \
                    or room.get_min_end_of_prog() < (self.current_v + Constants.T_SYNCHRO):
                r.append(room.id)
        return r

    def attach_observer(self, observer):
        for room in self.rooms:
            room.attach_observer(observer)

    def add_or_update_device(self, device_id):
        room_id = str(device_id)[0]
        for room in self.rooms:
            if room.id == room_id:
                room.add_or_update_device(device_id)

    def pop_or_reprogram_devices(self):
        for room in self.rooms:
            room.pop_or_reprogram_devices()

    def to_json_format(self):
        data = {"id": self.id, "rooms": []}

        for room in self.rooms:
            data["rooms"].append(room.to_json_format())

        return data
