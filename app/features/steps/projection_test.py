from behave import *
from hamcrest import *

import numpy


@given('a matrix')
def step_impl(context):
    context.matrix = numpy.arange(2, 11).reshape(3, 3)


@when('project the agent')
def step_impl(context):
    context.result = context.dpop_1.util_manager.project(context.matrix)


@then('result is a matrix has one less dimension')
def step_impl(context):
    assert_that(context.result.shape, equal_to((3,)))


@then('result contain optimal utility for agent value chosen')
def step_impl(context):
    for index, value in numpy.ndenumerate(context.result):
        assert_that(value, equal_to(min(context.matrix[:, index])))
