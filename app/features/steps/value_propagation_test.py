#! python3
# value_propagation_test.py - Test the VALUE Propagation behavior

from behave import *
from hamcrest import *

import numpy
import json

@when('get VALUE from parent after UTIL propagation')
def step_impl(context):
    set_up(context)

@then('should select the optimal assignment')
def step_impl(context):
    index = context.current_dpop_tested.getIndexOfBestValueWith(context.data, context.util_matrix)
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
    assert_that(calling(context.current_dpop_tested.getIndexOfBestValueWith).with_args(context.data, context.util_matrix), raises(Exception))
    
@when('matrix has 1 dimension')
def step_impl(context):
    set_up(context)
    context.util_matrix = numpy.asmatrix([[1],[0],[1]])

@then('should return the min value index')
def step_impl(context):
    index = context.current_dpop_tested.getIndexOfBestValueWith(context.data, context.util_matrix)
    assert_that(index, equal_to(1)) 

###
#   Privates Methods
###

def set_up(context):
    context.current_dpop_tested.matrix_dimensions = [1]
    context.util_matrix = numpy.arange(start=11, stop=2, step=-1).reshape(3, 3)
    context.data = {"1":1}
