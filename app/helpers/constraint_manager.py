
class ConstraintManager(object):

    INFINITY = 241
    URGT_TIME = 30
    T_SYNCHRO = 30
    THREE_HOURS = 180

    def __init__(self, room):
        self.room = room

    def get_cost_of_private_constraints_for_value(self, value):
        return self.c1_no_devices(value) \
               + self.c2_device_status(value) \
               + self.c4_last_intervention(value) \
               + self.c5_nothing_to_report(value)

    def c1_no_devices(self, vi):
        if self.room.has_no_devices() and vi < self.INFINITY:
            return self.INFINITY
        return 0

    def c2_device_status(self, vi):
        if self.room.is_in_critical_state() and vi > 0:
            return self.INFINITY

        min_end_of_prog = self.room.get_min_end_of_prog()

        if not self.room.is_in_critical_state() and min_end_of_prog <= self.URGT_TIME and vi > min_end_of_prog:
            return 1

        return 0

    def c3_neighbors_sync(self, vi, vj):
        diff = abs(vi - vj)
        if diff <= self.T_SYNCHRO and diff != 0:
            return 1
        return 0

    def c4_last_intervention(self, vi):
        if self.room.is_tau_too_high() and vi > self.URGT_TIME:
            return self.INFINITY
        return 0

    def c5_nothing_to_report(self, vi):
        if not self.room.is_in_critical_state() \
                and self.room.get_min_end_of_prog() > self.URGT_TIME \
                and self.room.tau < self.THREE_HOURS \
                and vi < self.INFINITY:
            return 1

        return 0
