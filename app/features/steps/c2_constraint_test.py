#! python3
# c2_constraint_test.py - Test the C2 constraint in dpop

from behave import *
from hamcrest import *
from model.device import Device


@when('an IoT device is ending its program in less then 30 minutes')
def step_impl(context):
    context.dpop_to_test.monitored_area.device_list = [Device(1, 29, False)]
    context.dpop_to_test.monitored_area.tau = 60


@then("AI in syringe pump should call healthcare professionals before the end of its program")
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=10)
    assert_that(context.dpop_to_test.monitored_area.current_v, less_than_or_equal_to(29))


@when("an IoT device is in critical state and ends its program in less then 30 minutes")
def step_impl(context):
    context.dpop_to_test.monitored_area.device_list = [Device(1, 30, False), Device(2, 241, True)]
