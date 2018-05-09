#! python3
# starter.py - Thread which gives "TOP" to the DPOP agents
# It is a thread intended to be launched by the server
from helpers.message_types import MessageTypes
from helpers.mqtt_manager import MQTTManager
from threading import Thread

import time
import json
import operator


class Starter(Thread):

    DIMENSION = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120, 180, 210, 241, 242]
    URGT_TIME = 30
    INFINITY_IDX = 16
    TWO_MINUTS = 120

    def __init__(self, agents, mqtt_client):

        Thread.__init__(self)

        self.agents = agents
        self.priorities = {}
        self.old_results_index = {}
        self.mqtt_manager = MQTTManager(mqtt_client)

        for agent in self.agents:
            self.priorities[str(agent.id)] = 0
            self.old_results_index[str(agent.id)] = self.INFINITY_IDX

    def run(self):

        while 1:

            print("--- START ALGORITHM ---")

            root = 0
            best_value = 0
            received_index = {}
    
            for agent in self.agents:
                self.mqtt_manager.publish_on_msg_to(agent.id)

            while len(self.mqtt_manager.client.list_msgs_waiting) < len(self.agents):
                # Wait for ROOTs messages
                pass

            for msg in self.mqtt_manager.client.list_msgs_waiting:
                splited = msg.split(":")
                if int(splited[1]) > best_value:
                    root = int(splited[0])
                    best_value = int(splited[1])

            self.mqtt_manager.client.list_msgs_waiting = []

            for agent in self.agents:
                self.mqtt_manager.publish_elected_root_msg_to(agent.id, root)

            while len(received_index) < len(self.agents):

                if self.mqtt_manager.has_no_msg():
                    # Wait for VALUES results
                    continue

                print("---", self.mqtt_manager.client.list_msgs_waiting)

                received_index.update(
                    json.loads(self.mqtt_manager.client.list_msgs_waiting.pop(0).split(MessageTypes.VALUES.value + " ")[1])
                )

            self.manage_priorities(received_index)

            print("--- RESULTS ---")

            sorted_priorities = sorted(self.priorities.items(), key=operator.itemgetter(1))
            for agent_id, priority in sorted_priorities:
                print("Room ", agent_id,
                      " need intervention in ", self.DIMENSION[received_index[agent_id]],
                      " minutes. PRIORITY : ", priority)
                self.old_results_index[agent_id] = received_index[agent_id]

            time.sleep(self.TWO_MINUTS)

    def manage_priorities(self, data_received):
        for key in data_received:

            if self.DIMENSION[self.old_results_index[key]] <= self.URGT_TIME \
                    and self.DIMENSION[data_received[key]] < self.URGT_TIME:
                self.priorities[key] += 1
            else:
                self.priorities[key] = 0
