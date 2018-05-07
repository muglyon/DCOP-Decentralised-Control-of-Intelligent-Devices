from unittest.mock import MagicMock
from behave import *
from hamcrest import *
from threads.starter import Starter


@given("a server interacting with AI agents")
def step_impl(context):
    context.server_thread = Starter([context.agent_1], MagicMock())


@when("an AI agent with priority 0 needs intervention in less then 30 minutes in two iterations in a row")
def step_impl(context):
    context.server_thread.priorities["1"] = 0
    context.server_thread.old_results["1"] = 3


@then("server should increase priority of this agent")
def step_impl(context):
    context.server_thread.manage_priorities({"1": 2})
    assert_that(context.server_thread.priorities["1"], greater_than(0))


@when("an AI agent with priority 5 does not need intervention anymore")
def step_impl(context):
    context.server_thread.priorities["1"] = 5
    context.server_thread.old_results["1"] = 3


@then("AI agent priority should be 0")
def step_impl(context):
    context.server_thread.manage_priorities({"1": 10})
    assert_that(context.server_thread.priorities["1"], equal_to(0))
