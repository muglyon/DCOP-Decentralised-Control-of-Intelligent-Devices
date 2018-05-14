#! python3
# server_main.py - Run the server for the DCOP system in the hospital
# It will do nothing if agents are not listening/running for the server signal !
# Usage: py.exe server_main.py - Run the server
from helpers import log
from model.hospital import Hospital
from mqtt.server_mqtt import ServerMQTT
from datetime import datetime


if __name__ == "__main__":

    # FOR DEBUG
    nb_agents = 6
    hospital = Hospital(nb_agents)

    log_file = "logs/server/log_server_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    log.setup_custom_logger(log_file)
    log.info('Server programmed for ' + str(nb_agents) + ' agents', 'DCOP/SERVER/')

    ServerMQTT(hospital).run()
