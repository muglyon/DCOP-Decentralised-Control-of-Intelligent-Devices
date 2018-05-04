#! python3
# common.py - Common step for testing

from behave import *
from hamcrest import *


@given('an AI agent')
def step_impl(context):
    context.current_dpop_tested = context.dpop_2


@given('an AI agent supervisor')
def step_impl(context):
    context.current_dpop_tested = context.dpop_1


@given('two neighbors AI agents')
def step_impl(context):
    context.current_dpop_tested = context.dpop_4
    assert_that(context.agent_4.leftNeighbor.id == context.agent_2.id
                or context.agent_4.rightNeighbor.id == context.agent_2.id)


@then('agent should not call health workers')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, equal_to(context.INFINITY))


@then('agent should call health workers right now')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, equal_to(0))
