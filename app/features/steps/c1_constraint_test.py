#! python3
# c1_nb_devices_constraint_test.py - Test the C1 constraint in dpop

from behave import *


@when('no IoT devices are connected to the AI in syringe pump')
def setp_impl(context):
    context.current_dpop_tested.room.set_devices([])
