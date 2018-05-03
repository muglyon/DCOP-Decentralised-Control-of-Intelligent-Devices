#! python3
# agent_main.py - Run an agent for a DCOP system in the hospital
# Usage: py.exe agent_main.py <agentId> - Run the agent number <agentId>

from model.hospital import Hospital
from model.room import Room
from dpop import Dpop

import paho.mqtt.client as mqtt
import sys

MQTT_SERVER = "10.33.120.194" #AVNET server address

###
# Callback mqtt connection
def on_connect(client, userdata, flags, rc):
    client.subscribe("DCOP/" + str(room.id) + "/#");
    print("Subscribe to DCOP/" + str(room.id) + "/#")

###
# Callback message arrived
# + Do the DPOP on "ON_<root>" demand
def on_message(client, userdata, msg):
    if "ON" in str(msg.payload) :
        thread = Dpop(room, client, str(room.id) in str(msg.payload))
        thread.start()
    else :
        client.listMessagesAttente.append(str(msg.payload.decode('utf-8')))
        print(msg.topic + " " + str(msg.payload))

###
# Callback for disconnection
def on_disconnect(client, userdata, rc=0):
    print("Disconnected result code :", rc)
    client.loop_stop()

if __name__ == "__main__" :

    ### FOR DEBUG : TO REMOVE !
    ## => Pas de devices pour le moment
    hospital = Hospital(6)

    for r in hospital.roomList:
        if r.id == int(sys.argv[1]):
            room = r
            break

    print(room.toString())

    client = mqtt.Client()
    client.listMessagesAttente = []
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()
