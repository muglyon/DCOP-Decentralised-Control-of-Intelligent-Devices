import time

from random import random
from threading import Thread
from constants import *


class Event(Thread):

    def __init__(self, monitored_area):
        Thread.__init__(self)
        self.deamon = True
        self.monitored_area = monitored_area

    def run(self):

        while 1:

            if random() < 0.05:
                self.generate_random_event()

            time.sleep(THIRTY_SECONDS)

    def generate_random_event(self):

        random_prob = random()

        if random_prob < 0.2 and not self.monitored_area.has_no_devices():
            self.monitored_area.set_device_in_critic()

        elif random_prob < 0.4:
            self.monitored_area.add_or_update_device()

        else:
            self.monitored_area.pop_or_reprogram_devices()

