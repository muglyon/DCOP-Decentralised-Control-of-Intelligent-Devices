#! python3
# dpop.py - Implement the DPOP Algorithm
# It is a thread intended to be launched by an agent
#
# /!\ WARNING /!\
# The objective in this case is to MINIMIZE all constraints.
import time

from copy import copy
from threading import Thread

from dcop_engine import execution_time
from dcop_engine.execution_time import *
from logs import log
from constants import Constants
from dcop_engine.constraint_manager import ConstraintManager
from dcop_engine.managers.dfs_manager import DfsManager
from dcop_engine.managers.value_manager import ValueManager
from dcop_engine.managers.util_manager import UtilManager
from mqtt.mqtt_manager import MQTTManager


def dpop_launch(monitored_area, client):
    thread = Dpop(monitored_area, client)
    thread.start()
    thread.join(timeout=10)


class Dpop(Thread):

    def __init__(self, monitored_area, mqtt_client):
        Thread.__init__(self)

        self.original_monitored_area = monitored_area  # Original
        self.monitored_area = copy(monitored_area)  # Copy to avoid multiple dcop_server access in the same time

        self.mqtt_manager = MQTTManager(mqtt_client, self.monitored_area)
        self.dfs_manager = DfsManager(self.mqtt_manager, self.monitored_area)
        self.util_manager = UtilManager(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = ValueManager(self.mqtt_manager, self.dfs_manager.dfs_structure)

    def run(self):

        log.execution_time = 0
        start_time = time.time()

        self.dfs_manager.generate_dfs(),
        self.util_manager.do_util_propagation(),
        self.value_manager.do_value_propagation(self.util_manager.JOIN, self.util_manager.UTIL)

        exec_time = time.time() - start_time

        self.original_monitored_area.current_v = self.monitored_area.current_v

        execution_time.total.append(exec_time)
        execution_time.for_dpop.append(
            exec_time - log.execution_time - self.dfs_manager.choose_root_execution_time
        )

        log.info("Avg size of msg RECEIVED (bytes) : " + str(self.mqtt_manager.client.avg_msg_size),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("Nb msg RECEIVED for this it : " + str(self.mqtt_manager.client.nb_msg_exchanged_current),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("Total Nb msg RECEIVED : " + str(self.mqtt_manager.client.nb_msg_exchanged_total),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("Avg Execution time TOTAL (s) : " + str(average(execution_time.total)),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("Avg Execution time dpop (s) : " + str(average(execution_time.for_dpop)),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("Interval de conf total 95% (s) : " + str(confidence_interval(execution_time.total)),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("Interval de conf dpop 95% (s) : " + str(confidence_interval(execution_time.for_dpop)),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("v = " + str(self.monitored_area.current_v),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("const val : " +
                 str(ConstraintManager()
                     .get_cost_of_private_constraints_for_value(self.monitored_area, self.monitored_area.current_v)
                     ),
                 self.monitored_area.id,
                 Constants.RESULTS)

        log.info("v rooms :"
                 + str([tuple([room.id, room.current_v]) for room in self.monitored_area.rooms]),
                 self.monitored_area.id,
                 Constants.RESULTS)
        #
        # log.info("rooms affected :"
        #          + str(self.monitored_area.get_room_who_need_intervention()),
        #          self.monitored_area.id,
        #          Constants.RESULTS)
