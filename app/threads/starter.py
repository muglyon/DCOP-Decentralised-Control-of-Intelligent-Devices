#! python3
# starter.py - Thread which gives "TOP" to the DPOP agents
# It is a thread intended to be launched by the server

from threading import Thread

import time


class Starter(Thread):

    def __init__(self, agents, mqtt_client):
        Thread.__init__(self)
        self.agents = agents
        self.mqtt_client = mqtt_client

    def run(self):

        while 1:

            print("--- START ALGORITHM ---")

            root = 0
            best_value = 0
    
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

            for agent in self.agents:
                self.mqtt_client.publish("DCOP/" + str(agent.id), "ROOT_" + str(root))
                
            time.sleep(120)  # 2 minutes
