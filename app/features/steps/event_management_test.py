from unittest import mock
from unittest.mock import MagicMock

from behave import *
from hamcrest import *

from constants import Constants
from events.event_observer import EventObserver
from logs.message_types import MessageTypes
from model.device import Device
from model.hospital import Hospital
from mqtt.server_mqtt import ServerMQTT
from dcop_engine.dpop import Dpop
from dcop_server.urgt_starter import UrgentStarter


@given("the event manager")
def step_impl(context):
    context.room_2.device_list = [Device(21, Constants.INFINITY, False)]

    context.event_manager = EventObserver(context.room_2, context.mock_clientMqtt_2)
    context.event_manager.mqtt_manager.publish_urgent_msg_to_server = MagicMock()

    context.room_2.attach_observer(context.event_manager)

    context.dpop_to_test = Dpop(context.room_2, context.mock_clientMqtt_2)


@when("a device of the room enter into a critical state")
def step_impl(context):
    context.room_2.device_list[0].is_in_critic_state = True


@when("a device enter into a critical state during calculation")
def step_impl(context):
    context.dpop_to_test.start()
    context.room_2.device_list[0].is_in_critic_state = True
    context.dpop_to_test.join(timeout=10)


@then("AI in syringe pump should send urgent message to server")
def step_impl(context):
    context.event_manager.mqtt_manager.publish_urgent_msg_to_server.assert_called_once_with(2)


@given("an mqtt server interacting with AI agents in syringe pump")
def step_impl(context):
    context.server_mqtt = ServerMQTT(Hospital(3))
    context.server_mqtt.starter = context.server_thread
    context.server_mqtt.starter.start = MagicMock()
    context.server_mqtt.starter.start()


@when("receive an 'URGT' message from AI in syringe pump")
def step_impl(context):

    with mock.patch('mqtt.custom_mqtt_class.CustomMQTTClass.on_message'):
        context.msg = MagicMock()
        context.msg.topic = "DCOP/SERVER/"
        context.msg.payload.decode.return_value = MessageTypes.URGT.value + "_" + str(3)


@then("server should send 'ON' messages to every AI in syringe pump")
def step_impl(context):
    with mock.patch('mqtt.mqtt_manager.MQTTManager.publish_on_msg_to'):
        with mock.patch('dcop_server.urgt_starter.UrgentStarter.get_values'):
            context.urgt_thread = context.server_mqtt.on_message(MagicMock(), MagicMock(), context.msg)
            context.urgt_thread.join(timeout=10)
            assert_that(context.urgt_thread, instance_of(UrgentStarter))
            assert_that(context.urgt_thread.mqtt_manager.publish_on_msg_to.call_count, equal_to(3))


@then("should choose the sender of the 'URGT' message as root")
def step_impl(context):
    with mock.patch('mqtt.mqtt_manager.MQTTManager.publish_elected_root_msg_to'):
        with mock.patch('dcop_server.urgt_starter.UrgentStarter.get_values'):
            context.urgt_thread = context.server_mqtt.on_message(MagicMock(), MagicMock(), context.msg)
            context.urgt_thread.join(timeout=10)
            assert_that(context.urgt_thread.mqtt_manager.publish_elected_root_msg_to.call_count, equal_to(3))
            context.urgt_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(1, 3)
            context.urgt_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(2, 3)
            context.urgt_thread.mqtt_manager.publish_elected_root_msg_to.assert_any_call(3, 3)


@then("server should give biggest priority to urgent agent and set next passage in 0 mins")
def step_impl(context):
    assert_that(context.server_mqtt.starter.priorities, equal_to({'1': 0, '2': 0, '3': 0}))

    with mock.patch('mqtt.mqtt_manager.MQTTManager.publish_elected_root_msg_to'):
        with mock.patch('dcop_server.urgt_starter.UrgentStarter.get_values'):
            context.urgt_thread = context.server_mqtt.on_message(MagicMock(), MagicMock(), context.msg)
            context.urgt_thread.join(timeout=10)

            biggest_prio = 0
            ai_prio = 1
            for key in context.server_mqtt.starter.priorities:
                if context.server_mqtt.starter.priorities[key] > biggest_prio:
                    biggest_prio = context.server_mqtt.starter.priorities[key]
                    ai_prio = key

            assert_that(ai_prio, equal_to(str(3)))
