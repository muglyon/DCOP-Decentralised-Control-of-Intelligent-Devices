#! python3
# c5_ras_constraint_test.py - Test c5 constraint in dpop

from behave import *
from hamcrest import *
from model.device import Device
from threads.dpop import Dpop


@when('there is nothing to report')
def step_impl(context):
    context.room_2.device_list = [Device(11, 40, False)]
    context.room_2.tau = 80

    context.dpop_to_test = Dpop(context.room_2, context.mock_clientMqtt_2)

    assert_that(not context.dpop_to_test.monitored_area.device_list[0].is_in_critic_state, 'device not in critical state')
    assert_that(context.dpop_to_test.monitored_area.device_list[0].end_of_prog > 30, 'device end its program too soon')
    assert_that(context.dpop_to_test.monitored_area.tau < 180, 'previous intervention is too recent')
