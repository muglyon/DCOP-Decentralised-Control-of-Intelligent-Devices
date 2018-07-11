#! python3
# hospital.py - Implement the environment model for testing/configuring

from math import *
from model.room import Room
from model.zone import Zone


class Hospital(object):

    def __init__(self, nb_zones, nb_rooms):

        self.zones = []

        # Version par chambre ?...
        self.monitored_area_list = []
        for i in range(0, nb_rooms):
            self.monitored_area_list.append(Room(i))
        self.setup_neighbors()

        for k in range(1, nb_zones + 1):
            self.zones.append(Zone(k))

        nb_rooms_by_zone = ceil(nb_rooms/nb_zones)
        count = 0
        zone_num = 0
        for j in range(0, nb_rooms):

            if count == nb_rooms_by_zone:
                count = 0
                zone_num += 1

            self.zones[zone_num].add_room(Room(j))
            count += 1

        self.setup_zone_neighbors()

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
                left_current.left_neighbor = right_current
                right_current.left_neighbor = left_current

            if k > 0:
                left_current.left_neighbor = left_side[k - 1]
                right_current.left_neighbor = right_side[k - 1]

            if k < moitie_agent - 1:
                left_current.right_neighbor = left_side[k + 1]
                right_current.right_neighbor = right_side[k + 1]

            if k == moitie_agent - 1:
                left_current.right_neighbor = right_current
                right_current.right_neighbor = left_current

            if 0 < k < moitie_agent - 1:
                left_current.front_neighbor = right_current
                right_current.front_neighbor = left_current

    def setup_zone_neighbors(self):

        moitie_zone = int(len(self.zones) / 2)
        left_side = self.zones[0:moitie_zone]
        right_side = self.zones[moitie_zone:len(self.zones)]

        for k in range(0, moitie_zone):

            left_current = left_side[k]
            right_current = right_side[k]

            if k == 0:
                left_current.left_neighbor = right_current
                right_current.left_neighbor = left_current

            if k > 0:
                left_current.left_neighbor = left_side[k - 1]
                right_current.left_neighbor = right_side[k - 1]

            if k < moitie_zone - 1:
                left_current.right_neighbor = left_side[k + 1]
                right_current.right_neighbor = right_side[k + 1]

            if k == moitie_zone - 1:
                left_current.right_neighbor = right_current
                right_current.right_neighbor = left_current

            if 0 < k < moitie_zone - 1:
                left_current.front_neighbor = right_current
                right_current.front_neighbor = left_current

    def to_string(self):
        string = ""
        for zone in self.zones:
            string += zone.to_json_format()
        return string
