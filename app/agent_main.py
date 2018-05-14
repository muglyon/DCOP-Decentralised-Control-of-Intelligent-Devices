#! python3
# agent_main.py - Run an agent for a DCOP system in the hospital
# Usage: py.exe agent_main.py <agentId> - Run the agent number <agentId>
from helpers import log
from model.hospital import Hospital
from mqtt.agent_mqtt import AgentMQTT
from datetime import datetime

import sys


if __name__ == "__main__":

    # FOR DEBUG : TO REMOVE !
    room = 0
    hospital = Hospital(6)

    for r in hospital.roomList:
        if r.id == int(sys.argv[1]):
            room = r
            break

    log_file = "logs/agents/log_agent_" + str(room.id) + "_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    log.setup_custom_logger(log_file)
    log.info(room.to_string(), "DCOP/" + str(room.id))

    AgentMQTT(room).run()
