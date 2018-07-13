from datetime import datetime

import time
import json
import numpy

from constants import Constants
from dcop_engine.managers.dpop_manager import DpopManager
from logs.message_types import MessageTypes
from logs import log


class ValueManager(DpopManager):

    def __init__(self, mqtt_manager, dfs_structure):
        DpopManager.__init__(self, mqtt_manager, dfs_structure)

    def do_value_propagation(self, join_matrix, util_list):
        log.info("Value Start", self.dfs_structure.monitored_area.id, Constants.INFO)

        values = []

        if util_list is None:
            util_list = []

        if not self.dfs_structure.is_root:
            self.mqtt_manager.publish_util_msg_to(
                self.dfs_structure.parent_id,
                json.dumps({Constants.VARS: "nothing here", Constants.DATA: util_list})
            )

            values = self.get_values_from_parents()

        # Find best v
        index = self.get_index_of_best_value_with(values, join_matrix)

        lowest_value = Constants.INFINITY

        print("INDEX : ", index)
        print("ROOMS : ", len(self.dfs_structure.monitored_area.rooms))

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
        while (time.time() - start_time) < Constants.TIMEOUT:
            if self.mqtt_manager.has_value_msg():
                return json.loads(self.mqtt_manager.client.value_msgs.pop(0).split(MessageTypes.VALUES.value + " ")[1])

        return dict()

    def get_index_of_best_value_with(self, data, join_list):

        if join_list is None:
            log.critical("List NULL pour la méthode dpop.getIndexOfBestValueWith(...)",
                         self.dfs_structure.monitored_area.id)
            return Constants.INFINITY_IDX

        if len(join_list) == 1:
            indices = [i for i, x in enumerate(join_list) if x == min(join_list)]
            return indices[len(indices) - 1]

        # print("DATA : ", data)
        # if not data:
        #     log.critical("Données manquantes pour la méthode dpop.getIndexOfBestValueWith(...)",
        #                  self.dfs_structure.monitored_area.id)
        #     return Constants.INFINITY_IDX

        # tup = self.extract_parent_values(data)
        # tup = self.extract_dependant_non_neighbors_values(data, join_list, tup)

        return self.find_best_index(join_list, data)

    def extract_parent_values(self, data):
        # Check for parents values
        all_parents_id = self.dfs_structure.pseudo_parents_id
        all_parents_id.append(self.dfs_structure.parent_id)
        tupl = tuple()

        for parent_id in all_parents_id:
            key = str(parent_id)
            if key in data:
                tupl = tupl + (data[key],)
        return tupl

    def find_best_index(self, join_matrix, tup):

        best_index = []
        best_value = Constants.INFINITY + 1

        print(join_matrix)
        print("TUP ", tup)

        nb_rooms = len(self.dfs_structure.monitored_area.rooms)

        for elements in join_matrix:
            cost = 0

            print("elements[:nb_rooms] : ", elements[:nb_rooms])

            for neighbors_element in elements[nb_rooms:]:
                if (neighbors_element[0] in t[0] and neighbors_element[1] in t[1] for t in tup):

                    print("tup find in element")
                    for sub_element in elements[:nb_rooms]:
                        print("sub : ", sub_element)
                        cost += sub_element[2]

            if cost <= best_value:
                best_index = elements[nb_rooms:]
                best_value = cost

        return best_index

    @staticmethod
    def extract_dependant_non_neighbors_values(data, join_list, tup):
        # Check for dependant non-neighbors values if needed

        # Todo : check that
        # for neighbor_id in matrix_dimensions_order:
        for neighbor_id in join_list:

            if len(join_list) - 1 == len(tup):
                break

            key = str(neighbor_id)
            if key in data:
                tup = tup + (data[key],)
        return tup
