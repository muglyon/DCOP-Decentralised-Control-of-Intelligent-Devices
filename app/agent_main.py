#! python3
# agent_main.py - Run an agent for a DCOP system in the hospital
# Usage: py.exe agent_main.py <agentId> - Run the agent number <agentId>

from model.hospital import Hospital
from mqtt.agent_mqtt import AgentMQTT

import sys

if __name__ == "__main__":

    # FOR DEBUG : TO REMOVE !
    hospital = Hospital(6)

    for r in hospital.roomList:
        if r.id == int(sys.argv[1]):
            room = r
            break

    print("\n", room.to_string())

    AgentMQTT(room).run()
