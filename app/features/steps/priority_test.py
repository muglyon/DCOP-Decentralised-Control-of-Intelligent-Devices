from unittest.mock import MagicMock
from behave import *
from hamcrest import *

from threads.starter import Starter


@given("a server interacting with AI agents in syringe pump")
def step_impl(context):
    context.server_thread = Starter([context.agent_1,
                                     context.agent_2,
                                     context.agent_3],
                                    MagicMock())


@when("an AI agent with priority 0 needs intervention in less then 30 minutes in two iterations in a row")
def step_impl(context):
    context.server_thread.priorities["1"] = 0
    context.server_thread.old_results_index["1"] = 3


@then("server should increase priority of this room")
def step_impl(context):
    context.server_thread.manage_priorities({"1": 2})
    assert_that(context.server_thread.priorities["1"], greater_than(0))


@when("an AI agent with priority 5 does not need intervention anymore")
def step_impl(context):
    context.server_thread.priorities["1"] = 5
    context.server_thread.old_results_index["1"] = 3


@then("AI agent priority should be 0")
def step_impl(context):
    context.server_thread.manage_priorities({"1": 10})
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
    context.server_thread.choose_root()


@then("server should choose the high-priority syringe as root")
def step_impl(context):
    assert_that(context.server_thread.mqtt_manager.publish_elected_root_msg_to.call_count, equal_to(3))
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(1, 3)
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(2, 3)
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(3, 3)
