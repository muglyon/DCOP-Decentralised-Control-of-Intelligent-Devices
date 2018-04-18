#! python3
# server_main.py - Run the server for the DCOP system in the hospital
# It will do nothing if agents are not listening/running for the server signal !
# Usage: py.exe server_main.py - Run the server

from model.hospital import Hospital
from model.device import Device

import paho.mqtt.client as mqtt

###
# Callback mqtt connection
def on_connect(client, userdata, flags, rc):
    print("Connected with the status " + str(rc))
    client.subscribe("DCOP/#");

###
# Callback message arrived
def on_message(client, userdata, msg):    
    print(msg.topic + " " + str(msg.payload))

###
# Heuristic for the DFS tree generation
# Return the agent with the max degree of neighbors
def getMaxDegreeAgent():
    
    maxDegree = 0
    maxDegreeAgentId = 0
    
    for room in hospital.roomList :
        degree = room.getDegree()
        if degree > maxDegree :
            maxDegree = degree
            maxDegreeAgentId = room.id

    return maxDegreeAgentId

if __name__ == "__main__" :

    nb_agents = 6

    hospital = Hospital(nb_agents)

    print('SERVER PREVU POUR ', nb_agents, ' AGENTS !')
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.33.120.194", 1883, 60)

    dfsRoot = getMaxDegreeAgent()
    
    for agent in hospital.roomList:
        client.publish("DCOP/" + str(agent.id), "ON_" + str(dfsRoot))

    client.loop_forever()
    

