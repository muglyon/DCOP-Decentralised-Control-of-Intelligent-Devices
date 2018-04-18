#! python3
# c3_neighborhood_constraint_test.py - Test c3 constraint in dpop

from behave import *
from hamcrest import *
from model.room import Room
from model.device import Device
from dpop import Dpop
from unittest.mock import MagicMock

@when('they call the nurse in almost the same time t1 and t2 with t1 > t2')
def step_impl(context):
    context.dpop_4.c1 = MagicMock(return_value=0)
    context.dpop_4.c5 = MagicMock()
    context.dpop_4.c5.side_effect = mocked_constraint_return_15
    context.dpop_4.start()
    context.dpop_4.join(timeout=10)

@then('agents should call the nurse together synchronized in t2')
def step_impl(context): 
    assert_that(context.dpop_4.v, equal_to(10))

@when('one is calling the nurse but not the other one')
def step_impl(context):
    context.dpop_4.c1 = MagicMock(return_value=0)
    context.dpop_4.c5 = MagicMock()
    context.dpop_4.c5.side_effect = mocked_constraint_return_241               
    context.dpop_4.start()
    context.dpop_4.join(timeout=10)

@then('agents should not be synchronized')
def step_impl(context): 
    assert_that(context.dpop_4.v, equal_to(context.INFINITY))


###
#   Privates Methods
###

def mocked_constraint_return_15(arg):
    if arg == 15 :
        return 0
    return 1

def mocked_constraint_return_241(arg):
    if arg == 241 :
        return 0
    return 1
