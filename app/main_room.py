#! python3
# main_room.py - Run an agent for a DCOP system in the hospital (Room Approach)
# Usage: py.exe main_room.py <agentId> - Run the room number <agentId>

from logs import log
from events.event_observer import EventObserver
from model.hospital import Hospital
from mqtt.agent_mqtt import AgentMQTT
from datetime import datetime
from events.event import Event

import sys
import constants as c


def main(hospital):

    monitored_area = None

    for m in hospital.monitored_area_list:
        if m.id == int(sys.argv[1]):
            monitored_area = m
            break

    log_file = "logs/agents/log_agent_" + str(monitored_area.id) + "_" + datetime.now().strftime("%Y-%m-%d") + ".json"

    log.setup_custom_logger(log_file)
    log.info(monitored_area.to_json_format(), monitored_area.id, c.STATE)

    agent_mqtt = AgentMQTT(monitored_area)

    monitored_area.attach_observer(EventObserver(monitored_area, agent_mqtt.client))
    Event(monitored_area).start()

    agent_mqtt.run()


if __name__ == "__main__":

    main(Hospital(c.NB_ROOMS))

