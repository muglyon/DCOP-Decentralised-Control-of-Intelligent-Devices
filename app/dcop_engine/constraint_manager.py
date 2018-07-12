from constants import Constants
from model.zone import Zone


class ConstraintManager(object):

    # def __init__(self):
        # self.monitored_area = monitored_area

    @staticmethod
    def c3_neighbors_sync(vi, vj):
        diff = abs(vi - vj)
        if 0 < diff <= Constants.T_SYNCHRO:
            return 1
        return 0

    @staticmethod
    def c1_no_devices(monitored_area, vi):
        if monitored_area.has_no_devices() and vi < Constants.INFINITY:
            return Constants.INFINITY
        return 0

    @staticmethod
    def c2_device_status(monitored_area, vi):

        if monitored_area.is_in_critical_state():
            if vi > 0:
                return Constants.INFINITY
        else:
            min_end_of_prog = monitored_area.get_min_end_of_prog()
            if min_end_of_prog <= Constants.URGT_TIME and vi > min_end_of_prog:
                return 1

        return 0

    @staticmethod
    def c4_last_intervention(monitored_area, vi):
        if monitored_area.is_tau_too_high() and vi > Constants.URGT_TIME:
            print("tau too high")
            return Constants.INFINITY
        return 0

    @staticmethod
    def c5_nothing_to_report(monitored_area, vi):

        if not monitored_area.is_in_critical_state() \
                and monitored_area.get_min_end_of_prog() > Constants.URGT_TIME \
                and monitored_area.tau < Constants.THREE_HOURS \
                and vi < Constants.INFINITY:
            return 1

        return 0

    def get_cost_of_private_constraints_for_value(self, monitored_area, value):
        if type(monitored_area) is Zone:
            return self.__get_cost_for_zone(monitored_area, value)

        return self.c1_no_devices(monitored_area, value) \
               + self.c2_device_status(monitored_area, value) \
               + self.c4_last_intervention(monitored_area, value) \
               + self.c5_nothing_to_report(monitored_area, value)

    def __get_cost_for_zone(self, monitored_area, value):

        cost = 0

        for room in monitored_area.rooms:

            if room.is_in_critical_state():
                print("critic_state")
                return 0 if value == 0 else Constants.INFINITY

            cost += self.c4_last_intervention(room, value)
            cost += self.c2_device_status(room, value)
            cost += self.c5_nothing_to_report(room, value)

        return cost if cost < Constants.INFINITY else Constants.INFINITY
