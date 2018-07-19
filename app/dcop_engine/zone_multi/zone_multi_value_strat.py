import time
import json

from constants import *
from dcop_engine.dpop_manager import DpopManager
from logs.message_types import MessageTypes
from logs import log


class ZoneMultiValueStrat(DpopManager):

    def __init__(self, mqtt_manager, dfs_structure):
        DpopManager.__init__(self, mqtt_manager, dfs_structure)

    def do_value_propagation(self, join_matrix, util_list):
        log.info("Value Start", self.dfs_structure.monitored_area.id, INFO)

        values = []

        if util_list is None:
            util_list = []

        if not self.dfs_structure.is_root:
            self.mqtt_manager.publish_util_msg_to(
                self.dfs_structure.parent_id,
                json.dumps({DATA: util_list})
            )

            values = self.get_values_from_parents()

        # Find best v
        index = self.find_best_index(join_matrix, values)
        lowest_value = INFINITY

        for i in range(0, len(index)):

            value = index[i][1]
            self.dfs_structure.monitored_area.rooms[i].current_v = value

            if value < lowest_value:
                lowest_value = value

        self.dfs_structure.monitored_area.current_v = lowest_value
        values.append(["Z" + str(self.dfs_structure.monitored_area.id), lowest_value])

        for child in self.dfs_structure.children_id:
            self.mqtt_manager.publish_value_msg_to(child, json.dumps(values))

        if self.dfs_structure.is_leaf():
            self.mqtt_manager.publish_value_msg_to_server(json.dumps(values))

    def get_values_from_parents(self):

        start_time = time.time()

        # MQTT wait for incoming message of type VALUE from parent
        while (time.time() - start_time) < TIMEOUT:
            if self.mqtt_manager.has_value_msg():
                return json.loads(
                    self.mqtt_manager.client.value_msgs.pop(0).split(MessageTypes.VALUES.value + " ")[1]
                )

        return []

    def find_best_index(self, join_matrix, tup):

        best_index = []
        best_value = INFINITY + 1
        nb_rooms = len(self.dfs_structure.monitored_area.rooms)

        for elements in join_matrix:

            cost = 0
            is_element_match_conditions = True

            for neighbors_element in elements[nb_rooms:]:
                for sub_tup in tup:
                    if neighbors_element[0] == sub_tup[0] and not neighbors_element[1] == sub_tup[1]:
                        is_element_match_conditions = False
                        break

            if is_element_match_conditions:

                for sub_element in elements[:nb_rooms]:
                    cost += sub_element[2]

                if cost <= best_value:
                    best_index = elements[:nb_rooms]
                    best_value = cost

        return best_index
