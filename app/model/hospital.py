#! python3
# hospital.py - Implement the environment model for testing/configuring

from model.monitoring_area import MonitoringArea


class Hospital(object):

    def __init__(self, size):
        self.monitored_area_list = []

        for i in range(1, size + 1):
            self.monitored_area_list.append(MonitoringArea(i))

        self.setup_neighbors()

    def setup_neighbors(self):
        """
        Setup Neighbors on two lines (cf. Java Code)
        """

        moitie_agent = int(len(self.monitored_area_list) / 2)
        left_side = self.monitored_area_list[0:moitie_agent]
        right_side = self.monitored_area_list[moitie_agent:len(self.monitored_area_list)]

        for k in range(0, moitie_agent):
            
            left_current = left_side[k]
            right_current = right_side[k]

            if k == 0:
                left_current.set_left_neighbor(right_current)
                right_current.set_left_neighbor(left_current)

            if k > 0:
                left_current.set_left_neighbor(left_side[k - 1])
                right_current.set_left_neighbor(right_side[k - 1])

            if k < moitie_agent - 1:
                left_current.set_right_neighbor(left_side[k + 1])
                right_current.set_right_neighbor(right_side[k + 1])

            if k == moitie_agent - 1:
                left_current.set_right_neighbor(right_current)
                right_current.set_right_neighbor(left_current)

            if k > 0 and k < moitie_agent - 1:
                left_current.set_front_neighbor(right_current)
                right_current.set_front_neighbor(left_current)

    def to_string(self):
        string = ""
        for monitored_area in self.monitored_area_list:
            string += monitored_area.to_json()
        return string
