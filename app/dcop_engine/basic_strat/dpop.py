import time

from copy import copy
from threading import Thread

from dcop_engine import execution_time
from dcop_engine.basic_strat.dfs_strat import DfsStrat
from dcop_engine.basic_strat.util_strat_abstract import UtilStratAbstract
from dcop_engine.basic_strat.value_strat_abstract import ValueStratAbstract
from dcop_engine.execution_time import *
from logs import log
from dcop_engine.constraint_manager import *
from constants import *
from mqtt.mqtt_manager import MQTTManager


class Dpop(Thread):

    def __init__(self, monitored_area, mqtt_client):
        Thread.__init__(self)

        self.original_monitored_area = monitored_area  # Original
        self.monitored_area = copy(monitored_area)  # Copy to avoid multiple dcop_server access in the same time

        self.mqtt_manager = MQTTManager(mqtt_client, self.monitored_area)

        self.dfs_manager = DfsStrat(self.mqtt_manager, self.monitored_area)
        self.util_manager = UtilStratAbstract(self.mqtt_manager, self.dfs_manager.dfs_structure)
        self.value_manager = ValueStratAbstract(self.mqtt_manager, self.dfs_manager.dfs_structure)

    def run(self):

        log.execution_time = 0
        start_time = time.time()

        self.do_dpop()
        self.original_monitored_area.current_v = self.monitored_area.current_v
        self.log_results(start_time)

    def do_dpop(self):
        self.dfs_manager.generate_dfs(),
        self.util_manager.do_util_propagation(),
        self.value_manager.do_value_propagation(self.util_manager.JOIN, self.util_manager.UTIL, None)

    def log_results(self, start_time):

        exec_time = time.time() - start_time

        execution_time.total.append(exec_time)
        execution_time.for_dpop.append(
            exec_time - log.execution_time - self.dfs_manager.choose_root_execution_time
        )

        log.info("Avg size of msg RECEIVED (bytes) : " + str(self.mqtt_manager.client.avg_msg_size),
                 self.monitored_area.id,
                 RESULTS)
        log.info("Nb msg RECEIVED for this it : " + str(self.mqtt_manager.client.nb_msg_exchanged_current),
                 self.monitored_area.id,
                 RESULTS)
        log.info("Total Nb msg RECEIVED : " + str(self.mqtt_manager.client.nb_msg_exchanged_total),
                 self.monitored_area.id,
                 RESULTS)
        log.info("Avg Execution time TOTAL (s) : " + str(average(execution_time.total)),
                 self.monitored_area.id,
                 RESULTS)
        log.info("Avg Execution time dpop (s) : " + str(average(execution_time.for_dpop)),
                 self.monitored_area.id,
                 RESULTS)
        log.info("Interval de conf total 95% (s) : " + str(confidence_interval(execution_time.total)),
                 self.monitored_area.id,
                 RESULTS)
        log.info("Interval de conf dpop 95% (s) : " + str(confidence_interval(execution_time.for_dpop)),
                 self.monitored_area.id,
                 RESULTS)
        log.info("v = " + str(self.monitored_area.current_v),
                 self.monitored_area.id,
                 RESULTS)
        log.info("const val : " +
                 str(get_cost_of_private_constraints_for_value(self.monitored_area, self.monitored_area.current_v)),
                 self.monitored_area.id,
                 RESULTS)
