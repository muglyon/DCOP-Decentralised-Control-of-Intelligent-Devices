#! python3
# c1_nb_devices_constraint_test.py - Test the C1 constraint in dpop

from behave import *
from hamcrest import *
from model.room import Room
from model.device import Device
from dpop import Dpop
from unittest.mock import MagicMock

@when('no devices are connected to this agent')
def setp_impl(context):
    context.current_dpop_tested.room.setDevices([])
    context.current_dpop_tested.c3 = MagicMock(return_value=0)
    context.current_dpop_tested.c5 = MagicMock(return_value=0)
