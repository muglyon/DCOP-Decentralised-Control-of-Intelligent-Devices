from constants import *
from model.zone import Zone


def c3_neighbors_sync(vi, vj):
    diff = abs(vi - vj)
    if 0 < diff <= T_SYNCHRO:
        return 1
    return 0


def c1_no_devices(monitored_area, vi):
    if monitored_area.has_no_devices() and vi < INFINITY:
        return INFINITY
    return 0


def c2_device_status(monitored_area, vi):

    if monitored_area.is_in_critical_state():
        if vi > 0:
            return INFINITY
    else:
        min_end_of_prog = monitored_area.get_min_end_of_prog()
        if min_end_of_prog <= URGT_TIME and vi > min_end_of_prog:
            return 1

    return 0


def c4_last_intervention(monitored_area, vi):
    if monitored_area.is_tau_too_high() and vi > URGT_TIME:
        return INFINITY
    return 0


def c5_nothing_to_report(monitored_area, vi):

    if not monitored_area.is_in_critical_state() \
            and monitored_area.get_min_end_of_prog() > URGT_TIME \
            and monitored_area.tau < THREE_HOURS \
            and vi < INFINITY:
        return 1

    return 0


def get_cost_of_private_constraints_for_value(monitored_area, value):
    if type(monitored_area) is Zone:
        return __get_cost_for_zone(monitored_area, value)

    return c1_no_devices(monitored_area, value) \
           + c2_device_status(monitored_area, value) \
           + c4_last_intervention(monitored_area, value) \
           + c5_nothing_to_report(monitored_area, value)


def __get_cost_for_zone(monitored_area, value):

    cost = 0

    for room in monitored_area.rooms:

        if room.is_in_critical_state():
            return 0 if value == 0 else INFINITY

        cost += c4_last_intervention(room, value)
        cost += c2_device_status(room, value)
        cost += c5_nothing_to_report(room, value)

    return cost if cost < INFINITY else INFINITY
