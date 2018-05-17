#! python3
# mqtt_test.py - Test agents communications through MQTT

from behave import *
from hamcrest import *
from unittest.mock import MagicMock


@when("receive UTIL message in DFS Generation")
def step_impl(context):
    context.msg_to_ignore = context.util_2
    context.list = context.dpop_to_test.mqtt_manager.client.util_msgs
    context.dpop_to_test.util_manager.do_util_propagation = MagicMock()
    context.dpop_to_test.value_manager.do_value_propagation = MagicMock()
    assert_that(context.dpop_to_test.mqtt_manager.client.util_msgs, has_item(context.msg_to_ignore))


@when("receive VALUE message in UTIL Propagation")
def step_impl(context):
    context.msg_to_ignore = context.value_2
    context.list = context.dpop_to_test.mqtt_manager.client.value_msgs
    context.dpop_to_test.dfs_manager.dfs_structure.children_id.append(4)
    context.dpop_to_test.dfs_manager.generate_dfs = MagicMock()
    context.dpop_to_test.value_manager.do_value_propagation = MagicMock()
    assert_that(context.dpop_to_test.mqtt_manager.client.value_msgs, has_item(context.msg_to_ignore))


@then("should ignore the message")
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=10)
    assert_that(context.list, has_item(context.msg_to_ignore))


@when("child does not send UTIL message before TIMEOUT")
def step_impl(context):
    context.dpop_to_test.dfs_manager.dfs_structure.children_id.append(4)
    context.dpop_to_test.mqtt_manager.client.util_msgs = []
    context.dpop_to_test.dfs_manager.generate_dfs = MagicMock()
    context.dpop_to_test.value_manager.do_value_propagation = MagicMock()
    assert_that(context.dpop_to_test.mqtt_manager.client.util_msgs, is_not(has_item(context.util_2)))


@then("agent should proceed to value propagation")
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=20)
    context.dpop_to_test.value_manager.do_value_propagation.assert_called_once()


@when("parent does not send VALUE message before TIMEOUT")
def step_impl(context):
    context.dpop_to_test.dfs_manager.dfs_structure.parent_id = 1
    context.dpop_to_test.mqtt_manager.client.value_msgs = []
    context.dpop_to_test.dfs_manager.generate_dfs = MagicMock()
    context.dpop_to_test.util_propagation = MagicMock()
    context.dpop_to_test.value_manager.get_index_of_best_value_with = MagicMock(return_value=0)
    context.dpop_to_test.value_manager.get_values_from_parents = MagicMock(return_value={})
    assert_that(context.dpop_to_test.mqtt_manager.client.value_msgs, is_not(has_item(context.value_2)))


@then("agent should proceed anyway")
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=20)
    assert_that(context.dpop_to_test.monitored_area.current_v, not_none())
