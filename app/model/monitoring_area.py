#! python3
# monitoring_area.py - Modelisation of a room

import operator
import abc

from random import randint
from constants import Constants


class MonitoringArea(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, id_monitored_area):
        self.id = id_monitored_area
        self.front_neighbor = None
        self.right_neighbor = None
        self.left_neighbor = None
        self.current_v = 0
        self.previous_v = 0
        self.tau = randint(Constants.MIN_TAU_VALUE, Constants.INFINITY)

    def get_neighbors_id_sorted(self):
        """
        Get all neighbors id of the agent sorted by degree (decreasing)
        :return: neighbors id list sorted by degree
        :rtype: list
        """
        return self.get_neighbors_id_sorted_except(-1)

    def get_neighbors_id_sorted_except(self, agent_id):
        """
        Get all neighbors id EXCEPT <agent_id>
        :param agent_id: id of the agent to ignore
        :type agent_id: integer
        :return: neighbors id list sorted by degree
        :rtype: list
        """
        neighbors = {}

        if self.left_neighbor is not None and self.left_neighbor.id != int(agent_id):
            neighbors[str(self.left_neighbor.id)] = self.left_neighbor.get_degree()

        if self.right_neighbor is not None and self.right_neighbor.id != int(agent_id):
            neighbors[str(self.right_neighbor.id)] = self.right_neighbor.get_degree()

        if self.front_neighbor is not None and self.front_neighbor.id != int(agent_id):
            neighbors[str(self.front_neighbor.id)] = self.front_neighbor.get_degree()

        neighbors = sorted(neighbors.items(), key=operator.itemgetter(1), reverse=True)
        return [int(x) for x, _ in neighbors]

    def get_degree(self):
        count = 0
        if self.left_neighbor is not None:
            count += 1
        if self.right_neighbor is not None:
            count += 1
        if self.front_neighbor is not None:
            count += 1
        return count

    def to_string_neighbors(self):
        """
        To String for Neighbors
        :return: neighbors in string format
        :rtype: string
        """
        string = "monitored_area " + str(self.id) + " : \n"

        if self.left_neighbor is not None:
            string += " | LeftNeighbor : " + str(self.left_neighbor.id) + "\n"

        if self.right_neighbor is not None:
            string += " | RightNeighbor : " + str(self.right_neighbor.id) + "\n"

        if self.front_neighbor is not None:
            string += " | FrontNeighbor : " + str(self.front_neighbor.id) + "\n"
        return string

    def to_json_format(self):

        data = {"id": self.id, "tau": self.tau, "devices": []}

        for device in self.device_list:
            data["devices"].append(device.to_json_format())

        return data



    @abc.abstractmethod
    def attach_observer(self, observer):
        return

    @abc.abstractmethod
    def add_or_update_device(self):
        return

    @abc.abstractmethod
    def pop_or_reprogram_devices(self):
        return

    @abc.abstractmethod
    def increment_time(self, minutes):
        return

    @abc.abstractmethod
    def has_no_devices(self):
        return

    @abc.abstractmethod
    def set_device_in_critic(self):
        return
