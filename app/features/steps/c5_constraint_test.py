#! python3
# c5_ras_constraint_test.py - Test c5 constraint in dpop

from behave import *
from hamcrest import *
from model.room import Room
from model.device import Device
from dpop import Dpop
from unittest.mock import MagicMock

@when('there is nothing to report')
def step_impl(context):
    context.agent_2.setDevices([Device(11, 40, False)])
    context.agent_2.tau = 80

    assert_that(not context.current_dpop_tested.room.deviceList[0].inCriticalState, 'device not in critical state')
    assert_that(context.current_dpop_tested.room.deviceList[0].endOfProgram > 30, 'device end its program too soon')
    assert_that(context.current_dpop_tested.room.tau < 180, 'previous intervention is too recent')

    context.current_dpop_tested = context.dpop_2
    context.current_dpop_tested.c1 = MagicMock(return_value=0)
    context.current_dpop_tested.c3 = MagicMock(return_value=0)
