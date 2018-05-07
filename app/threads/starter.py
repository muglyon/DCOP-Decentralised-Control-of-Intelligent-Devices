#! python3
# starter.py - Thread which gives "TOP" to the DPOP agents
# It is a thread intended to be launched by the server
from threading import Thread

import time
import json
import operator


class Starter(Thread):

    DIMENSION = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120, 180, 210, 241]
    URGT_TIME = 30
    INFINITY = 241

    def __init__(self, agents, mqtt_client):
        Thread.__init__(self)
        self.agents = agents
        self.mqtt_client = mqtt_client
        self.priorities = {}
        self.old_results = {}

        for agent in self.agents:
            self.priorities[str(agent.id)] = 0
            self.old_results[str(agent.id)] = self.INFINITY

    def run(self):

        while 1:

            print("--- START ALGORITHM ---")

            root = 0
            best_value = 0
            data_received = {}
    
            for agent in self.agents:
                self.mqtt_client.publish("DCOP/" + str(agent.id), "ON")

            while len(self.mqtt_client.listMessages) < len(self.agents):
                # Wait for ROOTs messages
                pass

            for msg in self.mqtt_client.listMessages:
                splited = msg.split(":")
                if int(splited[1]) > best_value:
                    root = int(splited[0])
                    best_value = int(splited[1])

            self.mqtt_client.listMessages = []

            for agent in self.agents:
                self.mqtt_client.publish("DCOP/" + str(agent.id), "ROOT_" + str(root))

            while len(data_received) < len(self.agents):

                if len(self.mqtt_client.listMessages) == 0:
                    # Wait for VALUES results
                    continue

                data_received.update(json.loads(self.mqtt_client.listMessages.pop(0).split("VALUES ")[1]))

            self.manage_priorities(data_received)

            print("--- RESULTS ---")

            sorted_priorities = sorted(self.priorities.items(), key=operator.itemgetter(1))
            for agent_id, priority in sorted_priorities:
                print("Room ", agent_id,
                      " need intervention in ", self.DIMENSION[data_received[agent_id]],
                      " minutes. PRIORITY : ", priority)
                self.old_results[agent_id] = self.DIMENSION[data_received[agent_id]]

            time.sleep(120)  # 2 minutes

    def manage_priorities(self, data_received):
        '''
        Update priority of agents if needed.
        '''
        for key in data_received:
            if self.DIMENSION[self.old_results[key]] <= self.URGT_TIME \
                    and self.DIMENSION[data_received[key]] < self.URGT_TIME:
                self.priorities[key] += 1
            else:
                self.priorities[key] = 0
