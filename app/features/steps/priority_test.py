from unittest.mock import MagicMock
from behave import *
from hamcrest import *


@when("an AI agent with priority 0 needs intervention in less then 30 minutes in two iterations in a row")
def step_impl(context):
    context.server_thread.priorities["1"] = 0
    context.server_thread.old_results_index["1"] = 3


@then("server should increase priority of this room")
def step_impl(context):
    context.server_thread.get_result_by_priority({"1": 2})
    assert_that(context.server_thread.priorities["1"], greater_than(0))


@when("an AI agent with priority 5 does not need intervention anymore")
def step_impl(context):
    context.server_thread.priorities["1"] = 5
    context.server_thread.old_results_index["1"] = 3


@then("AI agent priority should be 0")
def step_impl(context):
    context.server_thread.get_result_by_priority({"1": 10})
    assert_that(context.server_thread.priorities["1"], equal_to(0))


@given("a single syringe pump with bigger priority then the other")
def step_impl(context):
    context.server_thread.mqtt_manager.client.list_msgs_waiting = []
    context.server_thread.mqtt_manager.client.list_msgs_waiting.append("1:1")
    context.server_thread.mqtt_manager.client.list_msgs_waiting.append("2:2")
    context.server_thread.mqtt_manager.client.list_msgs_waiting.append("3:1")
    context.server_thread.priorities["1"] = 1
    context.server_thread.priorities["2"] = 1
    context.server_thread.priorities["3"] = 2
    context.server_thread.mqtt_manager.publish_elected_root_msg_to = MagicMock()


@when("the server choose the root")
def step_impl(context):
    context.server_thread.get_result_by_priority = MagicMock()
    context.server_thread.get_values = MagicMock()
    context.server_thread.do_one_iteration()


@then("server should choose the high-priority syringe as root")
def step_impl(context):
    assert_that(context.server_thread.mqtt_manager.publish_elected_root_msg_to.call_count, equal_to(3))
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(1, 3)
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(2, 3)
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(3, 3)
