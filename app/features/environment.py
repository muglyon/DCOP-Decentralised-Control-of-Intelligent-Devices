#! python3
# environment.py - Setup environment for BEHAVE testings
# For simplicity : Mqtt communications and DFS Generation are Mocked
# ----------------
# This is important to setup a "realistic" environment for testing
# If the environment is not correct, dpop algorithm will fail
# /!\ Pay specificly attention to the mocked DFS Generation results ! /!\
# ----------------
# Also, be aware that this is a basic setup that can be over written during specific setp_impl 

from behave import *
from model.room import Room
from unittest.mock import MagicMock
from dpop import Dpop

import json
import numpy
import paho.mqtt.client as mqtt

def before_scenario(context, scenario):

    context.INFINITY = 241
    context.util_2 = 'UTIL ' + json.dumps({"vars": [4, 1, 2], "data": numpy.zeros((17, 17), dtype = int).tolist()})
    context.value_2 = 'VALUES ' + json.dumps({"1":0})
    
    context.agent_1 = Room(1)
    context.agent_2 = Room(2)
    context.agent_3 = Room(3)
    context.agent_4 = Room(4)
    
    context.agent_1.setLeftNeighbor(context.agent_2)
    context.agent_1.setRightNeighbor(context.agent_3)

    context.agent_2.setLeftNeighbor(context.agent_4)
    context.agent_2.setRightNeighbor(context.agent_1)

    context.agent_3.setLeftNeighbor(context.agent_4)
    context.agent_3.setRightNeighbor(context.agent_1)

    context.agent_4.setRightNeighbor(context.agent_2)
    context.agent_4.setLeftNeighbor(context.agent_3)    
    
    context.mock_clientMqtt_1 = MagicMock()
    context.mock_clientMqtt_1.listMessagesAttente = []
    context.mock_clientMqtt_1.listMessagesAttente.append('UTIL ' + json.dumps({"vars": [4, 1, 2], "data": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]}))

    context.mock_clientMqtt_2 = MagicMock()
    context.mock_clientMqtt_2.listMessagesAttente = []
    context.mock_clientMqtt_2.listMessagesAttente.append('CHILD 1')
    context.mock_clientMqtt_2.listMessagesAttente.append('CHILD 4')
    context.mock_clientMqtt_2.listMessagesAttente.append(context.util_2)
    context.mock_clientMqtt_2.listMessagesAttente.append(context.value_2)

    context.mock_clientMqtt_4 = MagicMock()
    context.mock_clientMqtt_4.listMessagesAttente = []
    context.mock_clientMqtt_4.listMessagesAttente.append('UTIL ' + json.dumps({"vars": [4, 1], "data": numpy.zeros((17, 17), dtype = int).tolist()}))
    context.mock_clientMqtt_4.listMessagesAttente.append('VALUES ' + json.dumps({"1":2, "2":2}))

    context.dpop_1 = Dpop(context.agent_1, context.mock_clientMqtt_1, True)
    context.dpop_1.children.append(context.agent_2.id)
    context.dpop_1.pseudo_children.append(context.agent_3.id)
    context.dpop_1.generatePseudoTree = MagicMock()

    context.dpop_2 = Dpop(context.agent_2, context.mock_clientMqtt_2, False)
    context.dpop_2.TIMEOUT = 10

    context.dpop_4 = Dpop(context.agent_4, context.mock_clientMqtt_4, False)
    context.dpop_4.parent = context.agent_2.id
    context.dpop_4.children.append(context.agent_3.id)
    context.dpop_4.generatePseudoTree = MagicMock()

    
