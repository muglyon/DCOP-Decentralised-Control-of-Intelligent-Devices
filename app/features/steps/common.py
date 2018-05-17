#! python3
# common.py - Common step for testing

from behave import *
from hamcrest import *
from helpers.constants import Constants


@given('an AI in syringe pump')
def step_impl(context):
    context.dpop_to_test = context.dpop_2


@given('an AI in syringe pump (supervisor)')
def step_impl(context):
    context.dpop_to_test = context.dpop_1


@given('two AI in syringe pump in two separate rooms next to each other')
def step_impl(context):
    context.dpop_to_test = context.dpop_4
    assert_that(context.agent_4.left_neighbor.id == context.agent_2.id
                or context.agent_4.right_neighbor.id == context.agent_2.id)


@then('AI in syringe pump should not call healthcare professionals')
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=10)
    assert_that(context.dpop_to_test.monitored_area.current_v, equal_to(Constants.INFINITY))


@then('AI in syringe pump should call healthcare professionals right now')
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=10)
    assert_that(context.dpop_to_test.monitored_area.current_v, equal_to(0))
