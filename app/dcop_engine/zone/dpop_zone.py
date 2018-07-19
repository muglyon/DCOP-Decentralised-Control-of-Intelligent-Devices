from constants import RESULTS
from dcop_engine.dpop import Dpop
from dcop_engine.zone.zone_dfs_strat import ZoneDfsStrat
from dcop_engine.zone.zone_util_start import ZoneUtilStrat
from dcop_engine.zone.zone_value_strat import ZoneValueStrat
from logs import log


class DpopZone(Dpop):

    def __init__(self, monitored_area, mqtt_client):
        Dpop.__init__(self, monitored_area, mqtt_client)

        self.dfs_manager = ZoneDfsStrat(self.mqtt_manager, self.monitored_area)
        self.util_manager = ZoneUtilStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = ZoneValueStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)

    def do_dpop(self):

        self.dfs_manager.generate_dfs(),
        self.util_manager.do_util_propagation(),
        self.value_manager.do_value_propagation(
            self.util_manager.JOIN,
            self.util_manager.UTIL,
            self.util_manager.matrix_dimensions_order
        )

    def log_results(self, start_time):
        Dpop.log_results(self, start_time)

        log.info("rooms affected :"
                 + str(self.monitored_area.get_room_who_need_intervention()),
                 self.monitored_area.id,
                 RESULTS)
