#! python3
# common.py - Common step for testing

from behave import *
from hamcrest import *


@given('an AI in syringe pump')
def step_impl(context):
    context.current_dpop_tested = context.dpop_2


@given('an AI in syringe pump (supervisor)')
def step_impl(context):
    context.current_dpop_tested = context.dpop_1


@given('two AI in syringe pump in two separate rooms next to each other')
def step_impl(context):
    context.current_dpop_tested = context.dpop_4
    assert_that(context.agent_4.leftNeighbor.id == context.agent_2.id
                or context.agent_4.rightNeighbor.id == context.agent_2.id)


@then('AI in syringe pump should not call healthcare professionals')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, equal_to(context.INFINITY))


@then('AI in syringe pump should call healthcare professionals right now')
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.room.current_v, equal_to(0))
