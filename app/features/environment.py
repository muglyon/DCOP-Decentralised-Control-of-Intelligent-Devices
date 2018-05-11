#! python3
# environment.py - Setup environment for BEHAVE testings
# For simplicity : Mqtt communications and DFS Generation are Mocked
# ----------------
# This is important to setup a "realistic" environment for testing
# If the environment is not correct, dpop algorithm will fail
# /!\ Pay specificly attention to the mocked DFS Generation results ! /!\
# ----------------
# Also, be aware that this is a basic setup that can be over written during specific setp_impl
from helpers.constants import Constants
from model.room import Room
from unittest.mock import MagicMock
from threads.dpop import Dpop

import json
import numpy


def before_scenario(context, scenario):

    Constants.TIMEOUT = 10

    context.util_2 = 'UTIL ' + json.dumps({"vars": [4, 1, 2], "data": numpy.zeros((17, 17), float).tolist()})
    context.value_2 = 'VALUES ' + json.dumps({"1": 0})
    
    context.agent_1 = Room(1)
    context.agent_2 = Room(2)
    context.agent_3 = Room(3)
    context.agent_4 = Room(4)
    
    context.agent_1.set_left_neighbor(context.agent_2)
    context.agent_1.set_right_neighbor(context.agent_3)

    context.agent_2.set_left_neighbor(context.agent_4)
    context.agent_2.set_right_neighbor(context.agent_1)

    context.agent_3.set_left_neighbor(context.agent_4)
    context.agent_3.set_right_neighbor(context.agent_1)

    context.agent_4.set_right_neighbor(context.agent_2)
    context.agent_4.set_left_neighbor(context.agent_3)
    
    context.mock_clientMqtt_1 = MagicMock()
    context.mock_clientMqtt_1.util_msgs = []
    context.mock_clientMqtt_1.util_msgs\
        .append('UTIL ' + json.dumps({"vars": [4, 1, 2], "data": numpy.ones(17, float).tolist()}))

    context.mock_clientMqtt_2 = MagicMock()
    context.mock_clientMqtt_2.child_msgs = []
    context.mock_clientMqtt_2.util_msgs = []
    context.mock_clientMqtt_2.value_msgs = []
    context.mock_clientMqtt_2.list_msgs_waiting = []
    context.mock_clientMqtt_2.list_msgs_waiting.append('ROOT_1')
    context.mock_clientMqtt_2.child_msgs.append('CHILD 1')
    context.mock_clientMqtt_2.child_msgs.append('CHILD 4')
    context.mock_clientMqtt_2.util_msgs.append(context.util_2)
    context.mock_clientMqtt_2.value_msgs.append(context.value_2)

    context.mock_clientMqtt_4 = MagicMock()
    context.mock_clientMqtt_4.util_msgs = []
    context.mock_clientMqtt_4.value_msgs = []
    context.mock_clientMqtt_4.value_msgs.append('VALUES ' + json.dumps({"1": 0, "2": 2}))
    context.mock_clientMqtt_4.util_msgs\
        .append('UTIL ' + json.dumps({"vars": [4, 1], "data": numpy.ones((17, 17), float).tolist()}))

    context.dpop_1 = Dpop(context.agent_1, context.mock_clientMqtt_1)
    context.dpop_1.dfs_manager.dfs_structure.is_root = True
    context.dpop_1.dfs_manager.dfs_structure.children_id.append(context.agent_2.id)
    context.dpop_1.dfs_manager.dfs_structure.pseudo_children_id.append(context.agent_3.id)
    context.dpop_1.dfs_manager.generate_dfs = MagicMock()

    context.dpop_2 = Dpop(context.agent_2, context.mock_clientMqtt_2)

    context.dpop_4 = Dpop(context.agent_4, context.mock_clientMqtt_4)
    context.dpop_4.dfs_manager.dfs_structure.parent_id = context.agent_2.id
    context.dpop_4.dfs_manager.dfs_structure.children_id.append(context.agent_3.id)
    context.dpop_4.dfs_manager.generate_dfs = MagicMock()
