#! python3
# value_propagation_test.py - Test the VALUE Propagation behavior

from behave import *
from hamcrest import *

import numpy


@when('get VALUE from parent after UTIL propagation')
def step_impl(context):
    set_up(context)
    context.dpop_to_test.util_manager.JOIN = context.util_matrix


@then('should select the optimal assignment')
def step_impl(context):
    index = context.dpop_to_test.value_manager.get_index_of_best_value_with(
        context.data,
        context.dpop_to_test.util_manager.matrix_dimensions_order,
        context.dpop_to_test.util_manager.JOIN
    )
    assert_that(index, equal_to(2))


@when('parent send values to wrong format')
def step_impl(context):
    set_up(context)
    context.data = 'wrong format'


@when('matrix is Null')
def step_impl(context):
    set_up(context)
    context.util_matrix = None


@then('should raise an exception')
def step_impl(context):
    assert_that(calling(context.dpop_to_test.value_manager.get_index_of_best_value_with)
                .with_args(context.data, context.util_matrix), raises(Exception))


@when('matrix has 1 dimension')
def step_impl(context):
    set_up(context)
    context.dpop_to_test.util_manager.JOIN = numpy.asmatrix([[1], [0], [1]])


@then('should return the min value index')
def step_impl(context):
    index = context.dpop_to_test.value_manager.get_index_of_best_value_with(
        context.data,
        context.dpop_to_test.util_manager.matrix_dimensions_order,
        context.dpop_to_test.util_manager.JOIN
    )
    assert_that(index, equal_to(1)) 

###
#   Privates Methods
###


def set_up(context):
    context.dpop_to_test.util_manager.matrix_dimensions_order = [1]
    context.util_matrix = numpy.arange(start=11, stop=2, step=-1).reshape(3, 3)
    context.data = {"1": 1}
