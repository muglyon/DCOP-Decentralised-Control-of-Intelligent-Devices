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

    # def attach_observer(self, observer):
    #     for room in self.monitored_area_list:
    #         room.attach_observer(observer)
    #

    #
    # def get_neighbors_id_sorted(self):
    #     return self.get_neighbors_id_sorted_except(-1)
    #
    # def get_neighbors_id_sorted_except(self, agent_id):
    #     neighbors = {}
    #
    #     if self.left_neighbor is not None and self.left_neighbor.id != int(agent_id):
    #         neighbors[str(self.left_neighbor.id)] = self.left_neighbor.get_degree()
    #
    #     if self.right_neighbor is not None and self.right_neighbor.id != int(agent_id):
    #         neighbors[str(self.right_neighbor.id)] = self.right_neighbor.get_degree()
    #
    #     if self.front_neighbor is not None and self.front_neighbor.id != int(agent_id):
    #         neighbors[str(self.front_neighbor.id)] = self.front_neighbor.get_degree()
    #
    #     neighbors = sorted(neighbors.items(), key=operator.itemgetter(1), reverse=True)
    #     return [int(x) for x, _ in neighbors]

