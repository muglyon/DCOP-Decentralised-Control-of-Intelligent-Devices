#! python3
# c3_neighborhood_constraint_test.py - Test c3 constraint in dpop

from behave import *
from hamcrest import *
from unittest.mock import MagicMock
from helpers.constants import Constants


@when('both AI call healthcare professionals in almost the same time t1 and t2 with t1 > t2')
def step_impl(context):
    mock_constraints(context)
    context.dpop_to_test.util_manager.constraint_manager.c5_nothing_to_report\
        .side_effect = mocked_constraint_return_15


@then('AI in syringe pump should call healthcare professionals together synchronized in t2')
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=10)
    assert_that(context.dpop_to_test.monitored_area.current_v, equal_to(10))


@when('one is calling healthcare professionals but not the other one')
def step_impl(context):
    mock_constraints(context)
    context.dpop_to_test.util_manager.constraint_manager.c5_nothing_to_report\
        .side_effect = mocked_constraint_return_241


@then('only the AI who need intervention should call healthcare professionals')
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=10)
    assert_that(context.dpop_to_test.monitored_area.current_v, equal_to(Constants.INFINITY))


###
#   Privates Methods
###

def mock_constraints(context):
    context.dpop_to_test.util_manager.constraint_manager.c1_no_devices = MagicMock(return_value=0)
    context.dpop_to_test.util_manager.constraint_manager.c2_device_status = MagicMock(return_value=0)
    context.dpop_to_test.util_manager.constraint_manager.c4_last_intervention = MagicMock(return_value=0)
    context.dpop_to_test.util_manager.constraint_manager.c5_nothing_to_report = MagicMock()


def mocked_constraint_return_15(arg):
    if arg <= 15:
        return 0
    return 1


def mocked_constraint_return_241(arg):
    if arg <= 241:
        return 0
    return 1
