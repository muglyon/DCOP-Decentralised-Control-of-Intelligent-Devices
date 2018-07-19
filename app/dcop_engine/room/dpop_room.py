
from dcop_engine.dpop import Dpop
from dcop_engine.room.room_dfs_strat import RoomDfsStrat
from dcop_engine.room.room_util_start import RoomUtilStrat
from dcop_engine.room.room_value_strat import RoomValueStrat


class DpopRoom(Dpop):

    def __init__(self, monitored_area, mqtt_client):
        Dpop.__init__(self, monitored_area, mqtt_client)

        self.dfs_manager = RoomDfsStrat(self.mqtt_manager, self.monitored_area)
        self.util_manager = RoomUtilStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = RoomValueStrat(self.mqtt_manager, self.dfs_manager.dfs_structure)

    def do_dpop(self):

        self.dfs_manager.generate_dfs(),
        self.util_manager.do_util_propagation(),
        self.value_manager.do_value_propagation(
            self.util_manager.JOIN,
            self.util_manager.UTIL,
            self.util_manager.matrix_dimensions_order
        )
