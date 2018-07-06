from model.monitoring_area import MonitoringArea
from random import randint, random
from logs import log
from constants import Constants
from model.device import Device


class Room(MonitoringArea):

    def __init__(self, id):
        MonitoringArea.__init__(self, id)

        self.device_list = []

        for device_id in range(0, randint(0, self.MAX_NB_DEVICES)):
            self.add_or_update_device(device_id)

    def add_or_update_device(self, device_id):
        id_device = str(self.id) + str(device_id + 1)
        critic_state = random() < 0.05
        self.device_list.append(Device(int(id_device), randint(self.MIN_TAU_VALUE, self.INFINITY), critic_state))

    def pop_or_reprogram_devices(self):

        for device in self.device_list:

            random_number = random()

            if device.is_in_critic_state and random_number < 0.2:
                log.info("healthcare pro pop critical devices", self.id, Constants.EVENT)
                self.device_list.pop(self.device_list.index(device))
                continue

            log.info("healthcare pro reboot devices", self.id, Constants.EVENT)
            device.is_in_critic_state = False
            device.end_of_prog = Constants.INFINITY

    def has_no_devices(self):
        return len(self.device_list) == 0

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

    def attach_observer(self, observer):
        for device in self.device_list:
            device.observer = observer
