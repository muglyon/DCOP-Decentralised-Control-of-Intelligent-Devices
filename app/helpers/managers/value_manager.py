from datetime import datetime
from helpers.constants import Constants
from helpers.managers.dpop_manager import DpopManager
from helpers.message_types import MessageTypes

import numpy
import json


class ValueManager(DpopManager):

    def __init__(self, mqtt_manager, dfs_structure):
        DpopManager.__init__(self, mqtt_manager, dfs_structure)

    def do_value_propagation(self, matrix_dimensions_order, join_matrix, util_matrix):
        print("\n---------- VALUE PROPAGATION ----------")

        values = {}

        if util_matrix is None:
            util_matrix = numpy.zeros(Constants.DIMENSION_SIZE, int)

        if not self.dfs_structure.is_root:
            self.mqtt_manager.publish_util_msg_to(
                self.dfs_structure.parent_id,
                json.dumps({Constants.VARS: matrix_dimensions_order, Constants.DATA: util_matrix.tolist()})
            )

            values = self.get_values_from_parents()

        # Find best v
        index = self.get_index_of_best_value_with(values, matrix_dimensions_order, join_matrix)
        self.dfs_structure.room.current_v = Constants.DIMENSION[index]
        values[str(self.dfs_structure.room.id)] = index

        for child in self.dfs_structure.children_id:
            self.mqtt_manager.publish_value_msg_to(child, json.dumps(values))

        if self.dfs_structure.is_leaf():
            self.mqtt_manager.publish_value_msg_to_server(json.dumps(values))

    def get_values_from_parents(self):

        start_time = datetime.now()

        # MQTT wait for incoming message of type VALUE from parent
        while (datetime.now() - start_time).total_seconds() < Constants.TIMEOUT:
            if self.mqtt_manager.has_value_msg():
                return json.loads(self.mqtt_manager.client.value_msgs.pop(0).split(MessageTypes.VALUES.value + " ")[1])

    def get_index_of_best_value_with(self, data, matrix_dimensions_order, join_matrix):

        if join_matrix is None:
            raise Exception("Matrice NULL pour la méthode dpop.getIndexOfBestValueWith(...)")

        if len(join_matrix.shape) == 1 or join_matrix.shape[1] == 1:
            indices = [i for i, x in enumerate(join_matrix) if x == min(join_matrix)]
            return indices[len(indices) - 1]

        if data is None or not type(data) is dict:
            raise Exception("Données manquantes pour la méthode dpop.getIndexOfBestValueWith(...)")

        best_value = Constants.INFINITY + 1
        best_index = 0
        tupl = tuple()

        all_parents_id = self.dfs_structure.pseudo_parents_id
        all_parents_id.append(self.dfs_structure.parent_id)

        # Check for parents values
        for parent_id in all_parents_id:
            key = str(parent_id)
            if key in data:
                tupl = tupl + (data[key],)

        # Check for dependant non-neighbors values if needed
        for neighbor_id in matrix_dimensions_order:

            if len(join_matrix.shape) - 1 == len(tupl):
                break

            key = str(neighbor_id)
            if key in data:
                tupl = tupl + (data[key],)

        for index, value in numpy.ndenumerate(join_matrix):

            if tupl == index[1:]:
                if value <= best_value:
                    best_value = value
                    best_index = index[0]

        return best_index
