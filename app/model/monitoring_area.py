#! python3
# monitoring_area.py - Modelisation of a room
import random
import operator

from random import randint

from helpers.constants import Constants
from model.device import Device


class MonitoringArea(object):

    MIN_TAU_VALUE = 5
    MAX_NB_DEVICES = 6
    INFINITY = 241

    def __init__(self, id_monitored_area):
        self.id = id_monitored_area
        self.front_neighbor = None
        self.right_neighbor = None
        self.left_neighbor = None
        self.current_v = 0
        self.previous_v = 0
        self.tau = randint(self.MIN_TAU_VALUE, self.INFINITY)
        self.device_list = []

        for device_id in range(0, randint(0, self.MAX_NB_DEVICES)):
            self.add_new_device(device_id)

    def add_new_device(self, device_id):
        id_device = str(self.id) + str(device_id + 1)
        critic_state = random.random() < 0.05
        self.device_list.append(Device(int(id_device), randint(self.MIN_TAU_VALUE, self.INFINITY), critic_state))

    def increment_time(self, minutes):
        """
        Set + <minutes> to all devices
        (Also, simulate a health workers intervention)
        :param minutes: number of minutes to add
        :type minutes: integer
        """
        self.tau += minutes
        self.previous_v -= minutes

        for device in self.device_list:
            device.end_of_prog -= minutes

            if device.end_of_prog == self.INFINITY:
                self.tau = 0

        if random.random() < 0.5:
            self.add_new_device(len(self.device_list))

    def healthcare_pro_take_care_of_critical_devices(self):
        for device in self.device_list:
            if device.is_in_critic_state:
                if random.random() < 0.4:
                    self.device_list.pop(self.device_list.index(device))
                elif random.random() < 0.4:
                    device.is_in_critic_state = False
                    device.end_of_prog = Constants.INFINITY

    def has_no_devices(self):
        return len(self.device_list) == 0

    def is_in_critical_state(self):
        """
        Check if the room is in critical state
        :return: True if the room has at least one device in critical state, False otherwise
        :rtype: boolean
        """
        for device in self.device_list:
            if device.is_in_critic_state:
                return True
        return False

    def is_tau_too_high(self):
        """
        Check if the last passage was too long ago
        :return: True if the last passage was too long ago, False otherwise
        :rtype: boolean
        """
        return (len(self.device_list) > 5 and self.tau > 180) or (len(self.device_list) >= 1 and self.tau > 210)

    def get_min_end_of_prog(self):
        """
        Get the minimum time before a program ends
        :return: the minimum time in minutes
        :rtype: integer
        """
        minimum = 241
        for device in self.device_list:
            if device.end_of_prog < minimum:
                minimum = device.end_of_prog
        return minimum

    def get_degree(self):
        """
        Get number of neighbors
        :return: the degree of the room
        :rtype: integer
        """
        count = 0
        if self.left_neighbor is not None:
            count += 1
        if self.right_neighbor is not None:
            count += 1
        if self.front_neighbor is not None:
            count += 1
        return count

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

    def update_device(self, device):
        """
        Update state of the device
        If it's a new one, the device is added to the list
        :param device: device to update
        :type device: Device
        """
        is_device_exist = False

        for d in self.device_list:
            if d.id == device.id:
                device = d
                is_device_exist = True
                break

        if not is_device_exist:
            self.device_list.append(device)

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

    def attach_observer(self, observer):
        for device in self.device_list:
            device.observer = observer
