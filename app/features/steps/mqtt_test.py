#! python3
# mqtt_test.py - Test agents communications through MQTT

from behave import *
from hamcrest import *
from dpop import Dpop
from unittest.mock import MagicMock

import json
import numpy

@when("receive UTIL message in DFS Generation")
def step_impl(context):
    context.msg_to_ignore = context.util_2
    context.current_dpop_tested.utilPropagation = MagicMock()
    context.current_dpop_tested.valuePropagation = MagicMock()
    assert_that(context.current_dpop_tested.mqttClient.listMessagesAttente, has_item(context.msg_to_ignore))

@when("receive VALUE message in UTIL Propagation")
def step_impl(context):
    context.msg_to_ignore = context.value_2
    context.current_dpop_tested.children.append(4)
    context.current_dpop_tested.generatePseudoTree = MagicMock()
    context.current_dpop_tested.valuePropagation = MagicMock()
    assert_that(context.current_dpop_tested.mqttClient.listMessagesAttente, has_item(context.msg_to_ignore))
    
@then("should ignore the message")
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.current_dpop_tested.mqttClient.listMessagesAttente, has_item(context.msg_to_ignore))
   
@when("child does not send UTIL message before TIMEOUT")
def step_impl(context):
    context.current_dpop_tested.children.append(4)
    context.current_dpop_tested.mqttClient.listMessagesAttente = []
    context.current_dpop_tested.generatePseudoTree = MagicMock()
    context.current_dpop_tested.valuePropagation = MagicMock()
    assert_that(context.current_dpop_tested.mqttClient.listMessagesAttente, is_not(has_item(context.util_2)))

@then("agent should proceed to value propagation")
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=20)
    context.current_dpop_tested.valuePropagation.assert_called_once_with()

@when("parent does not send VALUE message before TIMEOUT")
def step_impl(context):
    context.current_dpop_tested.parent = 1
    context.current_dpop_tested.mqttClient.listMessagesAttente = []
    context.current_dpop_tested.generatePseudoTree = MagicMock()
    context.current_dpop_tested.utilPropagation = MagicMock()
    context.current_dpop_tested.getIndexOfBestValueWith = MagicMock()
    assert_that(context.current_dpop_tested.mqttClient.listMessagesAttente, is_not(has_item(context.value_2)))

@then("agent should proceed anyway")
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=20)
    assert_that(context.current_dpop_tested.v, is_not(equal_to(None)))
