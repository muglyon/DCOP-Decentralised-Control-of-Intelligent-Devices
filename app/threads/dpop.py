#! python3
# dpop.py - Implement the DPOP Algorithm
# It is a thread intended to be launched by an agent
#
# /!\ WARNING /!\
# The objective in this case is to MINIMIZE all constraints.

from threading import Thread

from helpers.constants import Constants
from helpers.constraint_manager import ConstraintManager
from helpers.managers.dfs_manager import DfsManager
from helpers.managers.value_manager import ValueManager
from helpers import log
from mqtt.mqtt_manager import MQTTManager
from helpers.managers.util_manager import UtilManager


class Dpop(Thread):

    def __init__(self, monitored_area, mqtt_client):
        Thread.__init__(self)
        self.monitored_area = monitored_area
        self.mqtt_manager = MQTTManager(mqtt_client, self.monitored_area)
        self.dfs_manager = DfsManager(self.mqtt_manager, self.monitored_area)
        self.util_manager = UtilManager(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = ValueManager(self.mqtt_manager, self.dfs_manager.dfs_structure)

    def run(self):
        """
        /!\ Do the DPOP Algorithm /!\
        """
        self.dfs_manager.generate_dfs()
        self.util_manager.do_util_propagation()
        self.value_manager.do_value_propagation(self.util_manager.matrix_dimensions_order,
                                                self.util_manager.JOIN,
                                                self.util_manager.UTIL)

        log.info("v = " + str(self.monitored_area.current_v), self.monitored_area.id, Constants.RESULTS)
        log.info("const vals : " +
                 str(ConstraintManager(self.monitored_area)
                     .get_cost_of_private_constraints_for_value(self.monitored_area.current_v)),
                 self.monitored_area.id,
                 Constants.RESULTS)
