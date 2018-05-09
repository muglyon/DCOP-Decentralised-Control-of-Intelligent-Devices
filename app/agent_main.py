#! python3
# agent_main.py - Run an agent for a DCOP system in the hospital
# Usage: py.exe agent_main.py <agentId> - Run the agent number <agentId>

from model.hospital import Hospital
from threads.dpop import Dpop
from datetime import datetime
from helpers.messageTypes import MessageTypes

import paho.mqtt.client as mqtt
import sys

MQTT_SERVER = "10.33.120.194"
MQTT_PORT = 1883
KEEP_ALIVE_PERIOD = 60


def on_connect(client, userdata, flags, rc):
    """
    CallBack MQTT Connection
    """
    client.subscribe("DCOP/" + str(room.id) + "/#")
    print("Subscribe to DCOP/" + str(room.id) + "/#")


def on_message(client, userdata, msg):
    """
    CallBack Message Arrive
    - Do the DPOP on "ON" demand
    """

    global counter, start_time
    str_msg = str(msg.payload.decode('utf-8'))

    if str_msg == MessageTypes.ON.value:

        print("---------- ITERATION ", counter, " --------")

        if counter > 0:
            room.increment_time(int((datetime.now() - start_time).total_seconds() / 60))
            room.previous_v = room.current_v
            start_time = datetime.now()
            print("\n", room.to_string())

        thread = Dpop(room, client)
        thread.start()
        thread.join(timeout=10)
        counter += 1

    elif MessageTypes.CHILD.value in str_msg or MessageTypes.PSEUDO.value in str_msg:
        client.child_msgs.append(str_msg)
    elif MessageTypes.UTIL.value in str_msg:
        client.util_msgs.append(str_msg)
    elif MessageTypes.VALUES.value in str_msg:
        client.value_msgs.append(str_msg)
    else:
        client.list_msgs_waiting.append(str_msg)

    print(msg.topic + " " + str_msg)


def on_disconnect(client, userdata, rc=0):
    """
    CallBack when disconnection
    """
    print("Disconnected result code :", rc)
    client.loop_stop()


if __name__ == "__main__":

    # FOR DEBUG : TO REMOVE !
    hospital = Hospital(6)

    for r in hospital.roomList:
        if r.id == int(sys.argv[1]):
            room = r
            break

    print("\n", room.to_string())
    counter = 0
    start_time = datetime.now()

    client = mqtt.Client()

    client.list_msgs_waiting = []
    client.child_msgs = []
    client.util_msgs = []
    client.value_msgs = []

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(MQTT_SERVER, MQTT_PORT, KEEP_ALIVE_PERIOD)
    client.loop_forever()
