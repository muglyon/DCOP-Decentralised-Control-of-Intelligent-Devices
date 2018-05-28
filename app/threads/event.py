import time

from random import random
from threading import Thread
from helpers.constants import Constants
from helpers import log


class Event(Thread):

    def __init__(self, monitored_area):
        Thread.__init__(self)
        self.deamon = True
        self.monitored_area = monitored_area

    def run(self):

        while 1:

            if random() < 0.1:
                self.generate_random_event()

            time.sleep(Constants.FIVE_SECONDS)

    def generate_random_event(self):

        random_prob = random()

        if random_prob < 0.2 and not self.monitored_area.has_no_devices():
            self.monitored_area.device_list[0].is_in_critic_state = True
        elif random_prob < 0.4:
            log.info("nurse take care of devices", self.monitored_area.id, Constants.INFO)
            self.monitored_area.healthcare_pro_take_care_of_critical_devices()
