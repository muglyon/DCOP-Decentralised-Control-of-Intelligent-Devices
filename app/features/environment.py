#! python3
# environment.py - Setup environment for BEHAVE testings
# For simplicity : some methods are Mocked but those tests are INTEGRATION tests.
# ----------------
# This is important to setup a "realistic" environment for testing
# If the environment is not correct, DPOP algorithm will fail
# /!\ Pay specific attention to the mocked DFS Generation results ! /!\
# ----------------
# Also, be aware that this is a basic setup that can be over written during specific step_impl
import json
import numpy

from logs import log
from model.monitoring_area import MonitoringArea
from unittest.mock import MagicMock
from dcop_engine.basic_strat.dpop import Dpop


def before_scenario(context, scenario):

    TIMEOUT = 10

    context.util_2 = 'UTIL ' + json.dumps({"vars": [4, 1, 2], "data": numpy.zeros((17, 17), float).tolist()})
    context.value_2 = 'VALUES ' + json.dumps({"1": 0})
    
    context.room_1 = MonitoringArea(1)
    context.room_2 = MonitoringArea(2)
    context.room_3 = MonitoringArea(3)
    context.room_4 = MonitoringArea(4)
    
    context.room_1.left_neighbor = context.room_2
    context.room_1.right_neighbor = context.room_3

    context.room_2.left_neighbor = context.room_4
    context.room_2.right_neighbor = context.room_1

    context.room_3.left_neighbor = context.room_4
    context.room_3.right_neighbor = context.room_1

    context.room_4.right_neighbor = context.room_2
    context.room_4.left_neighbor = context.room_3

    log.info = MagicMock()
    log.critical = MagicMock()
    
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

    context.dpop_1 = Dpop(context.room_1, context.mock_clientMqtt_1)
    context.dpop_1.dfs_manager.dfs_structure.is_root = True
    context.dpop_1.dfs_manager.dfs_structure.children_id.append(context.room_2.id)
    context.dpop_1.dfs_manager.dfs_structure.pseudo_children_id.append(context.room_3.id)
    context.dpop_1.dfs_manager.generate_dfs = MagicMock()

    context.dpop_2 = Dpop(context.room_2, context.mock_clientMqtt_2)

    context.dpop_4 = Dpop(context.room_4, context.mock_clientMqtt_4)
    context.dpop_4.dfs_manager.dfs_structure.parent_id = context.room_2.id
    context.dpop_4.dfs_manager.dfs_structure.children_id.append(context.room_3.id)
    context.dpop_4.dfs_manager.generate_dfs = MagicMock()
