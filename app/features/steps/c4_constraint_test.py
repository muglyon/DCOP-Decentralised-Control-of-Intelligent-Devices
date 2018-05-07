#! python3
# c4_constraint_test.py - Test c4 constraint in dpop

from behave import *
from hamcrest import *
from model.device import Device


@when('the room contains more then 5 devices and last passage was more then 3 hours ago')
def step_impl(context):
    context.current_dpop_tested.room.set_devices([Device(1, 240, False),
                                                  Device(2, 240, False),
                                                  Device(3, 240, False),
                                                  Device(4, 240, False),
                                                  Device(5, 240, False),
                                                  Device(6, 240, False)])
    context.current_dpop_tested.room.tau = 181


@when('the room contains less then 5 devices and last passage was more then 3 hours ago')
def step_impl(context):
    context.current_dpop_tested.room.set_devices([Device(1, 240, False), Device(2, 240, False)])
    context.current_dpop_tested.room.tau = 181


@when('the room contains less then 5 devices and last passage was more then 4 hours ago')
def step_impl(context):
    context.current_dpop_tested.room.set_devices([Device(1, 240, False), Device(2, 240, False)])
    context.current_dpop_tested.room.tau = 211


@then('AI should call healthcare professionals in less then 30 minutes')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, less_than_or_equal_to(30))
