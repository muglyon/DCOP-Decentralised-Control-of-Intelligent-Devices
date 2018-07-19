from constants import RESULTS
from dcop_engine.room.dpop_room import DpopRoom
from logs import log


class DpopZone(DpopRoom):

    def __init__(self, monitored_area, mqtt_client):
        DpopRoom.__init__(self, monitored_area, mqtt_client)

    def log_results(self, start_time):
        DpopRoom.log_results(self, start_time)

        log.info("rooms affected :"
                 + str(self.monitored_area.get_room_who_need_intervention()),
                 self.monitored_area.id,
                 RESULTS)
