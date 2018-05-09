#! python3
# room.py - Modelisation of a room

from model.device import Device
from random import randint

import random
import operator


class Room(object):

    MAX_NB_DEVICES = 6

    def __init__(self, id_room):
        self.id = id_room
        self.frontNeighbor = None
        self.rightNeighbor = None
        self.leftNeighbor = None
        self.current_v = 0
        self.previous_v = 0
        self.tau = randint(5, 241)
        self.device_list = []

        for i in range(0, randint(0, self.MAX_NB_DEVICES)):
            id_device = str(self.id) + str(i + 1)
            critic_state = random.random() < 0.05
            self.device_list.append(Device(int(id_device), randint(5, 241), critic_state))

    def set_left_neighbor(self, neighbor):
        self.leftNeighbor = neighbor

    def set_right_neighbor(self, neighbor):
        self.rightNeighbor = neighbor

    def set_front_neighbor(self, neighbor):
        self.frontNeighbor = neighbor

    def set_devices(self, devices):
        self.device_list = devices

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
            if device.is_in_critic_state:
                if random.random() < 0.5:
                    self.device_list.pop(self.device_list.index(device))
                else:
                    device.is_in_critic_state = False
                    device.set_end_of_prog(241)
            else:
                device.set_end_of_prog(device.end_of_prog - minutes)

            if device.end_of_prog == 241:
                self.tau = 0

        # Randomly add a new device
        if random.random() < 0.5:
            id_device = str(self.id) + str(len(self.device_list) + 1)
            critic_state = random.random() < 0.05
            self.device_list.append(Device(int(id_device), randint(5, 241), critic_state))

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
        if self.leftNeighbor is not None:
            count += 1
        if self.rightNeighbor is not None:
            count += 1
        if self.frontNeighbor is not None:
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

        if self.leftNeighbor is not None and self.leftNeighbor.id != int(agent_id):
            neighbors[str(self.leftNeighbor.id)] = self.leftNeighbor.get_degree()

        if self.rightNeighbor is not None and self.rightNeighbor.id != int(agent_id):
            neighbors[str(self.rightNeighbor.id)] = self.rightNeighbor.get_degree()

        if self.frontNeighbor is not None and self.frontNeighbor.id != int(agent_id):
            neighbors[str(self.frontNeighbor.id)] = self.frontNeighbor.get_degree()

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

        if is_device_exist:
            pass
        else:
            self.device_list.append(device)

    def to_string_neighbors(self):
        """
        To String for Neighbors
        :return: neighbors in string format
        :rtype: string
        """
        string = "ROOM " + str(self.id) + " : \n"

        if self.leftNeighbor is not None:
            string += " | LeftNeighbor : " + str(self.leftNeighbor.id) + "\n"

        if self.rightNeighbor is not None:
            string += " | RightNeighbor : " + str(self.rightNeighbor.id) + "\n"

        if self.frontNeighbor is not None:
            string += " | FrontNeighbor : " + str(self.frontNeighbor.id) + "\n"
        return string

    def to_string(self):
        string = "ROOM " + str(self.id) + " : \n"
        string += "Tau : " + str(self.tau) + "\n"

        for device in self.device_list:
            string += device.to_string()

        return string