#! python3
# c5_ras_constraint_test.py - Test c5 constraint in dpop

from behave import *
from hamcrest import *
from model.device import Device


@when('there is nothing to report')
def step_impl(context):
    context.agent_2.set_devices([Device(11, 40, False)])
    context.agent_2.tau = 80

    context.dpop_to_test = context.dpop_2

    assert_that(not context.dpop_to_test.room.device_list[0].is_in_critic_state, 'device not in critical state')
    assert_that(context.dpop_to_test.room.device_list[0].end_of_prog > 30, 'device end its program too soon')
    assert_that(context.dpop_to_test.room.tau < 180, 'previous intervention is too recent')
