#! python3
# c3_neighborhood_constraint_test.py - Test c3 constraint in dpop

from behave import *
from hamcrest import *
from unittest.mock import MagicMock


@when('they call health workers in almost the same time t1 and t2 with t1 > t2')
def step_impl(context):
    mock_constraints(context)
    context.current_dpop_tested.c5.side_effect = mocked_constraint_return_15


@then('agents should call health workers together synchronized in t2')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, equal_to(10))


@when('one is calling health workers but not the other one')
def step_impl(context):
    mock_constraints(context)
    context.current_dpop_tested.c5.side_effect = mocked_constraint_return_241               


@then('agents should not be synchronized')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, equal_to(context.INFINITY))


###
#   Privates Methods
###

def mock_constraints(context):
    context.current_dpop_tested.c1 = MagicMock(return_value=0)
    context.current_dpop_tested.c2 = MagicMock(return_value=0)
    context.current_dpop_tested.c4 = MagicMock(return_value=0)
    context.current_dpop_tested.c5 = MagicMock()


def mocked_constraint_return_15(arg):
    if arg <= 15:
        return 0
    return 1


def mocked_constraint_return_241(arg):
    if arg <= 241:
        return 0
    return 1
