#! python3
# join_test.py - Test JOIN operator

from behave import *
from hamcrest import *

import numpy

@given('two matrix')
def step_impl(context):
    context.matrix_1 = numpy.ones((5, 5), dtype=int)
    context.matrix_2 = numpy.ones((5, 5), dtype=int)

@when('they have the same dimensions')
def step_impl(context):
    assert_that(context.matrix_1.shape, equal_to(context.matrix_2.shape))

@then('join operation should return matrix with dimension + 1')
def step_impl(context):
    result = context.dpop_1.combine(context.matrix_1, context.matrix_2)
    assert_that(result.shape, equal_to((5, 5, 5)))

@when('they do not have the same dimensions')
def step_impl(context):
    context.matrix_1 = numpy.ones((5, 5, 5), dtype=int)
    assert_that(context.matrix_1.shape, is_not(equal_to(context.matrix_2.shape)))

@then('join operation should return matrix with biggest matrix dimension + 1')
def step_impl(context):
    result = context.dpop_1.combine(context.matrix_1, context.matrix_2)
    assert_that(result.shape, equal_to((5, 5, 5, 5)))

@then('each joined matrix value is the sum of the corresponding cells in the two source matrices')
def step_impl(context):
    result = context.dpop_1.combine(context.matrix_1, context.matrix_2)
    for index, value in numpy.ndenumerate(result):
        val_1 = context.matrix_1[index[0], index[1]]
        val_2 = context.matrix_2[index[0], index[2]]
        assert_that(value, equal_to(val_1 + val_2))

@when('one of them is Null')
def step_impl(context):
    context.null_matrix = None

@then('join operation should return the other matrix (or raise an exception if both are Null)')
def step_impl(context):
    assert_that(context.dpop_1.combine(context.null_matrix, context.matrix_2), same_instance(context.matrix_2))
    assert_that(context.dpop_1.combine(context.matrix_1, context.null_matrix), same_instance(context.matrix_1))
    assert_that(calling(context.dpop_1.combine).with_args(context.null_matrix, context.null_matrix), raises(Exception))
