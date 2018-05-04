#! python3
# c2_constraint_test.py - Test the C2 constraint in dpop

from behave import *
from hamcrest import *
from model.device import Device


@when('a device is ending its program in less then 30 minutes')
def step_impl(context):
    context.current_dpop_tested.room.set_devices([Device(1, 29, False)])
    context.current_dpop_tested.room.tau = 60


@then("agent should call the nurse before the end of its program")
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, less_than_or_equal_to(29))


@when("device is in critical state and ends its program in less then 30 minutes")
def step_impl(context):
    context.current_dpop_tested.room.set_devices([Device(1, 30, False), Device(2, 241, True)])
