from constants import RESULTS
from dcop_engine.dpop import Dpop
from dcop_engine.zone_multi.zone_multi_dfs_strat import ZoneMultiDfsStrat
from dcop_engine.zone_multi.zone_multi_value_strat import ZoneMultiValueStrat
from dcop_engine.zone_multi.zone_multi_util_start import ZoneMultiUtilStrat
from logs import log


class DpopZone(Dpop):

    def __init__(self, monitored_area, mqtt_client):
        Dpop.__init__(self, monitored_area, mqtt_client)

        self.dfs_manager = ZoneMultiDfsStrat(self.mqtt_manager, self.monitored_area)
        self.util_manager = ZoneMultiUtilStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = ZoneMultiValueStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)

    def log_results(self, start_time):
        Dpop.log_results(self, start_time)

        log.info("v rooms :"
                 + str([tuple([room.id, room.current_v]) for room in self.monitored_area.rooms]),
                 self.monitored_area.id,
                 RESULTS)
