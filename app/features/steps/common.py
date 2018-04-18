#! python3
# common.py - Common step for testing

from behave import *
from hamcrest import *
from dpop import Dpop

@given('an IA agent')
def step_impl(context):
    context.current_dpop_tested = context.dpop_2

@given('an IA agent supervisor')
def step_impl(context):
    context.current_dpop_tested = context.dpop_1

@given('two neighbors IA agents')
def step_impl(context):
    assert_that(context.agent_4.leftNeighbor.id == context.agent_2.id or context.agent_4.rightNeighbor.id == context.agent_2.id)

@then('agent should not call the nurse')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.v, equal_to(context.INFINITY))
