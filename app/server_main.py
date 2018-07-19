#! python3
# server_main.py - Run the server for the DCOP system in the hospital
# It will do nothing if agents are not listening/running for the server signal !
# Usage: py.exe server_main.py - Run the server
from logs import log
from constants import *
from model.hospital import Hospital
from mqtt.server_mqtt import ServerMQTT
from datetime import datetime


if __name__ == "__main__":

    hospital = Hospital(NB_ROOMS, NB_ZONES)

    log_file = "logs/server/log_server_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    log.setup_custom_logger(log_file)
    log.info('Programmed for ' + str(NB_ROOMS) + ' agents', SERVER, INFO)

    ServerMQTT(hospital).run()
