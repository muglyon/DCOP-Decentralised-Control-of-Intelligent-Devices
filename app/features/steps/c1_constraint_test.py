#! python3
# c1_nb_devices_constraint_test.py - Test the C1 constraint in dpop

from behave import *


@when('no IoT devices are connected to the AI in syringe pump')
def step_impl(context):
    context.dpop_to_test.room.set_devices([])
