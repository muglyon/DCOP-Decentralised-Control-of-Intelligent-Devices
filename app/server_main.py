#! python3
# server_main.py - Run the server for the DCOP system in the hospital
# It will do nothing if agents are not listening/running for the server signal !
# Usage: py.exe server_main.py - Run the server

from model.hospital import Hospital
from threads.starter import Starter

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    """
    CallBack MQTT Connection
    """
    print("Connected with the status " + str(rc))
    client.subscribe("DCOP/#")
    thread = Starter(hospital.roomList, client)
    thread.start()


def on_message(client, userdata, msg):
    """
    CallBack Msg Arrive
    """
    data = str(msg.payload)
    print(msg.topic + " " + str(msg.payload))
    if "SERVER" in msg.topic:
        client.listMessages.append(str(msg.payload.decode('utf-8')))


if __name__ == "__main__":

    # FOR DEBUG
    nb_agents = 6
    hospital = Hospital(nb_agents)
    print('SERVER PREVU POUR ', nb_agents, ' AGENTS !')

    client = mqtt.Client()
    client.listMessages = []
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.33.120.194", 1883, 60)
    client.loop_forever()