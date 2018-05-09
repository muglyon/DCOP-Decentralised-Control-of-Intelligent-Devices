#! python3
# server_main.py - Run the server for the DCOP system in the hospital
# It will do nothing if agents are not listening/running for the server signal !
# Usage: py.exe server_main.py - Run the server

from model.hospital import Hospital
from mqtt.server_mqtt import ServerMQTT

if __name__ == "__main__":

    # FOR DEBUG
    nb_agents = 6
    hospital = Hospital(nb_agents)
    print('SERVEUR PREVU POUR ', nb_agents, ' AGENTS !')

    ServerMQTT(hospital).run()
