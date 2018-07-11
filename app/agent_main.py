#! python3
# agent_main.py - Run an agent for a DCOP system in the hospital
# Usage: py.exe agent_main.py <agentId> - Run the agent number <agentId>
from logs import log
from constants import Constants
from events.event_observer import EventObserver
from model.hospital import Hospital
from mqtt.agent_mqtt import AgentMQTT
from datetime import datetime

import sys

from events.event import Event

if __name__ == "__main__":

    monitored_area = None
    hospital = Hospital(Constants.NB_ZONES, Constants.NB_ROOMS)

    # /!\ Zones /!\
    for r in hospital.zones:
        if r.id == int(sys.argv[1]):
            monitored_area = r
            break

    # /!\ Rooms /!\
    # for r in hospital.monitored_area_list:
    #     if r.id == int(sys.argv[1]):
    #         monitored_area = r
    #         break

    print(monitored_area.to_json_format())

    log_file = "logs/agents/log_agent_" + str(monitored_area.id) + "_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    log.setup_custom_logger(log_file)
    log.info(monitored_area.to_json_format(), monitored_area.id, Constants.STATE)

    agent_mqtt = AgentMQTT(monitored_area)

    monitored_area.attach_observer(EventObserver(monitored_area, agent_mqtt.client))
    Event(monitored_area).start()

    agent_mqtt.run()
