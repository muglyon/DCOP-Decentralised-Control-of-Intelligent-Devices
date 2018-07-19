#! python3
# main_zone_multi.py - Run an agent for a DCOP system in the hospital (Multivariables Zone Approach)
# Usage: py.exe main_zone_multi.py <agentId> - Run the zone number <agentId>

from constants import *
from model.hospital import Hospital
from main_room import main

if __name__ == "__main__":

    main(Hospital(NB_ROOMS, NB_ZONES))
