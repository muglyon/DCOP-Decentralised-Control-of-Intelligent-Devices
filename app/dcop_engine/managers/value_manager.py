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

        values = dict()

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
        # self.dfs_structure.monitored_area.current_v = Constants.DIMENSION[index]
        # values[str(self.dfs_structure.monitored_area.id)] = index
        #
        # for child in self.dfs_structure.children_id:
        #     self.mqtt_manager.publish_value_msg_to(child, json.dumps(values))
        #
        # if self.dfs_structure.is_leaf():
        #     self.mqtt_manager.publish_value_msg_to_server(json.dumps(values))

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

        if data is None or not isinstance(data, dict):
            log.critical("Données manquantes pour la méthode dpop.getIndexOfBestValueWith(...)",
                         self.dfs_structure.monitored_area.id)
            return Constants.INFINITY_IDX

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
        nb_rooms = len(self.dfs_structure.monitored_area.rooms)

        # for index, value in numpy.ndenumerate(join_matrix):
        #     if tup == index[1:] and value <= best_value:
        #         best_value = value
        #         best_index = index[0]

        print(join_matrix)
        print("TUP ", tup)

        for elements in join_matrix:
            cost = 0
            bool = True

            print("elem : ", elements)

            for sub_element in elements[:-1]:

                print("sub : ", sub_element)

                if tup in elements and sub_element[1][0:2] in tup:
                    cost += sub_element[-1][2]
                else:
                    bool = False
                    break

            if cost <= best_value:
                best_index = elements
                best_value = cost

        print("Value chosen : ", best_index)
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
