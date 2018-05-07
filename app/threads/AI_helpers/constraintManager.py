
class ConstraintManager(object):

    INFINITY = 241
    URGT_TIME = 30
    T_SYNCHRO = 30

    def __init__(self, room):
        self.room = room

    def get_value_of_private_constraints_for_value(self, value):
        return self.c1(value) + self.c2(value) + self.c4(value) + self.c5(value)

    def c1(self, vi):
        if len(self.room.device_list) == 0 and vi < self.INFINITY:
            return self.INFINITY
        return 0

    def c2(self, vi):
        if self.room.is_in_critical_state() and vi > 0:
            return self.INFINITY

        x = self.room.get_min_end_of_prog()
        if not self.room.is_in_critical_state() and x <= self.URGT_TIME and vi > x:
            return 1

        return 0

    def c3(self, vi, vj):
        val = abs(vi - vj)
        if val <= self.T_SYNCHRO and val != 0:
            return 1
        return 0

    def c4(self, vi):
        if self.room.is_tau_too_high() and vi > self.URGT_TIME:
            return self.INFINITY
        return 0

    def c5(self, vi):
        if not self.room.is_in_critical_state() \
                and self.room.get_min_end_of_prog() > self.URGT_TIME \
                and self.room.tau < 180 \
                and vi < self.INFINITY:
            return 1

        return 0
