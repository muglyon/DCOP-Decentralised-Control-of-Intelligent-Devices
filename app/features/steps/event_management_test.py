from unittest.mock import MagicMock

from behave import *
from hamcrest import *

from helpers.constants import Constants
from helpers.event_manager import EventManager
from helpers.message_types import MessageTypes
from model.device import Device


@given("the event manager")
def step_impl(context):
    context.dpop_2.monitored_area.device_list = [Device(21, Constants.INFINITY, False)]

    context.event_manager = EventManager(context.dpop_2.monitored_area, context.mock_clientMqtt_2)
    context.event_manager.mqtt_manager.publish_urgent_msg_to_server = MagicMock()

    context.dpop_2.monitored_area.attach_observer(context.event_manager)

    context.dpop_to_test = context.dpop_2


@when("a device of the room enter into a critical state")
def step_impl(context):
    context.room_2.device_list[0].is_in_critic_state = True


@when("a device enter into a critical state during calculation")
def step_impl(context):
    context.dpop_to_test.start()
    context.dpop_to_test.join(timeout=10)
    context.room_2.device_list[0].is_in_critic_state = True


@then("AI in syringe pump should send urgent message to server")
def step_impl(context):
    context.event_manager.mqtt_manager.publish_urgent_msg_to_server.assert_called_once_with(2)


@when("receive an 'URGT' message from AI in syringe pump")
def step_impl(context):
    context.server_thread.mqtt_manager.client.urgent_msg_list = []
    context.server_thread.mqtt_manager.client.urgent_msg_list.append(MessageTypes.URGT.value + "_" + str(2))

    context.server_thread.mqtt_manager.publish_on_msg_to = MagicMock()
    context.server_thread.mqtt_manager.publish_elected_root_msg_to = MagicMock()
    context.server_thread.get_values = MagicMock()


@then("server should send 'ON' messages to every AI in syringe pump")
def step_impl(context):
    context.server_thread.manage_urgent_msg()
    assert_that(context.server_thread.mqtt_manager.publish_on_msg_to.call_count, equal_to(3))


@then("should choose the sender of the 'URGT' message as root")
def step_impl(context):
    assert_that(context.server_thread.mqtt_manager.publish_elected_root_msg_to.call_count, equal_to(3))
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(1, 2)
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(2, 2)
    context.server_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(3, 2)


