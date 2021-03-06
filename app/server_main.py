#! python3
# server_main.py - Run the server for the DCOP system in the hospital
# It will do nothing if agents are not listening/running for the server signal !
# Usage: py.exe server_main.py room - Run the server for "room" approach
#        py.exe server_main.py zone - Run the server for a "zone" approach
#        py.exe server_main.py multi - Run the server for a "multi variables zone" approach

from logs import log
from model.hospital import Hospital
from mqtt.server_mqtt import ServerMQTT
from datetime import datetime

import sys
import constants as c


if __name__ == "__main__":

    hospital = Hospital(c.NB_ROOMS, c.NB_ZONES, True)
    parameter = str(sys.argv[1])

    if "room" in parameter:
        hospital = Hospital(c.NB_ROOMS)
    elif "zone" in parameter:
        hospital = Hospital(c.NB_ROOMS, c.NB_ZONES)

    log_file = "logs/server/log_server_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    log.setup_custom_logger(log_file)
    log.info('Programmed for ' + str(c.NB_ROOMS) + ' agents', c.SERVER, c.INFO)

    ServerMQTT(hospital).run()
