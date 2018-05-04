#! python3
# mqtt_test.py - Test agents communications through MQTT

from behave import *
from hamcrest import *
from unittest.mock import MagicMock


@when("receive UTIL message in DFS Generation")
def step_impl(context):
    context.msg_to_ignore = context.util_2
    context.list = context.current_dpop_tested.mqtt_client.util_msgs
    context.current_dpop_tested.util_propagation = MagicMock()
    context.current_dpop_tested.value_propagation = MagicMock()
    assert_that(context.current_dpop_tested.mqtt_client.util_msgs, has_item(context.msg_to_ignore))


@when("receive VALUE message in UTIL Propagation")
def step_impl(context):
    context.msg_to_ignore = context.value_2
    context.list = context.current_dpop_tested.mqtt_client.value_msgs
    context.current_dpop_tested.children.append(4)
    context.current_dpop_tested.generate_pseudo_tree = MagicMock()
    context.current_dpop_tested.value_propagation = MagicMock()
    assert_that(context.current_dpop_tested.mqtt_client.value_msgs, has_item(context.msg_to_ignore))


@then("should ignore the message")
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=10)
    assert_that(context.list, has_item(context.msg_to_ignore))


@when("child does not send UTIL message before TIMEOUT")
def step_impl(context):
    context.current_dpop_tested.children.append(4)
    context.current_dpop_tested.mqtt_client.util_msgs = []
    context.current_dpop_tested.generate_pseudo_tree = MagicMock()
    context.current_dpop_tested.value_propagation = MagicMock()
    assert_that(context.current_dpop_tested.mqtt_client.util_msgs, is_not(has_item(context.util_2)))


@then("agent should proceed to value propagation")
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=20)
    context.current_dpop_tested.value_propagation.assert_called_once_with()


@when("parent does not send VALUE message before TIMEOUT")
def step_impl(context):
    context.current_dpop_tested.parent = 1
    context.current_dpop_tested.mqtt_client.value_msgs = []
    context.current_dpop_tested.generate_pseudo_tree = MagicMock()
    context.current_dpop_tested.util_propagation = MagicMock()
    context.current_dpop_tested.get_index_of_best_value_with = MagicMock(return_value=0)
    assert_that(context.current_dpop_tested.mqtt_client.value_msgs, is_not(has_item(context.value_2)))


@then("agent should proceed anyway")
def step_impl(context):
    context.current_dpop_tested.start()
    context.current_dpop_tested.join(timeout=20)
    assert_that(context.current_dpop_tested.room.current_v, not_none())
