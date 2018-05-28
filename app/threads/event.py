import time

from random import random
from threading import Thread

from helpers.constants import Constants


class Event(Thread):

    def __init__(self, monitored_area):
        Thread.__init__(self)
        self.deamon = True
        self.monitored_area = monitored_area

    def run(self):

        while 1:

            if random() < 0.5:
                self.generate_random_event()

            time.sleep(Constants.FIVE_SECONDS)

    def generate_random_event(self):

        random_prob = random()

        if random_prob < 0.05 and not self.monitored_area.has_no_devices():
            self.monitored_area.device_list[0].is_in_critic_state = True
        elif random_prob < 0.4:
            print("nurse take care of devices")
            self.monitored_area.healthcare_pro_take_care_of_critical_devices()
