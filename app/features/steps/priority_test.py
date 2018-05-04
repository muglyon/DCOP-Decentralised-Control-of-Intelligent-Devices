# from behave import *
# from hamcrest import *
# from model.device import Device
#
# import json
#
#
# @given("two non neighbors AI agents (a1, a2) calling nurses and linked by another AI agent (a3)")
# def step_impl(context):
#     # (cf : environment.py)
#     # a1 = dpop_1
#     # a2 = dpop_4
#     # a3 = dpop_2
#     context.dpop_1.room.tau = 100
#     context.dpop_4.room.tau = 100
#     context.dpop_1.room.set_devices([Device(11, 20, False)])
#     context.dpop_4.room.set_devices([Device(41, 20, False)])
#
#
# @when("a1's priority > a2's priority and a3 does not need intervention")
# def step_impl(context):
#     context.dpop_1.room.priority = 5
#     context.dpop_4.room.priority = 2
#     context.dpop_4.mqtt_client.value_msgs = ['VALUES ' + json.dumps({"1": 4, "2": 16})]
#     print(context.dpop_1.room.to_string())
#     print(context.dpop_4.room.to_string())
#
#
# @then("nurses should intervene in room 1 before room 2")
# def step_impl(context):
#     context.dpop_1.start()
#     context.dpop_4.start()
#     context.dpop_1.join(timeout=10)
#     context.dpop_4.join(timeout=10)
#     print(context.dpop_1.JOIN)
#     print(context.dpop_4.JOIN)
#     print(context.dpop_4.UTIL)
#     assert_that(context.dpop_1.room.current_v, less_than(context.dpop_4.room.current_v))
#
#
# @when("a1's priority = a2's priority and a3 does not need intervention")
# def step_impl(context):
#     context.dpop_1.room.priority = 1
#     context.dpop_4.room.priority = 1
#     context.dpop_4.mqtt_client.value_msgs = ['VALUES ' + json.dumps({"1": 0, "2": 16})]
#     assert_that(context.dpop_1.room.priority, equal_to(context.dpop_4.room.priority))
#
#
# @then("both agent should call the nurse at the same time")
# def step_impl(context):
#     context.dpop_1.start()
#     context.dpop_4.start()
#     context.dpop_1.join(timeout=10)
#     context.dpop_4.join(timeout=10)
#     assert_that(context.dpop_1.room.current_v, equal_to(context.dpop_4.room.current_v))
#
