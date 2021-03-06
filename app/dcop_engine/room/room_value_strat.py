import time
import json
import numpy
import constants as c

from dcop_engine.basic_strat.value_strat_abstract import ValueStratAbstract
from logs.message_types import MessageTypes
from logs import log


class RoomValueStrat(ValueStratAbstract):

    def __init__(self, mqtt_manager, dfs_structure):
        ValueStratAbstract.__init__(self, mqtt_manager, dfs_structure)

    def do_value_propagation(self, join_matrix, util_matrix, matrix_dimensions_order):
        log.info("Value Start", self.dfs_structure.monitored_area.id, c.INFO)

        values = dict()

        if util_matrix is None:
            util_matrix = numpy.zeros(c.DIMENSION_SIZE, int)

        if not self.dfs_structure.is_root:
            self.mqtt_manager.publish_util_msg_to(
                self.dfs_structure.parent_id,
                json.dumps({c.VARS: matrix_dimensions_order, c.DATA: util_matrix.tolist()})
            )

            values = self.get_values_from_parents()

        # Find best v
        index = self.get_index_of_best_value_with(values, matrix_dimensions_order, join_matrix)
        self.dfs_structure.monitored_area.current_v = c.DIMENSION[index]
        values[str(self.dfs_structure.monitored_area.id)] = index

        for child in self.dfs_structure.children_id:
            self.mqtt_manager.publish_value_msg_to(child, json.dumps(values))

        if self.dfs_structure.is_leaf():
            self.mqtt_manager.publish_value_msg_to_server(json.dumps(values))

    def get_values_from_parents(self):

        start_time = time.time()

        # MQTT wait for incoming message of type VALUE from parent
        while (time.time() - start_time) < c.TIMEOUT:
            if self.mqtt_manager.has_value_msg():
                return json.loads(self.mqtt_manager.client.value_msgs.pop(0).split(MessageTypes.VALUES.value + " ")[1])

        return dict()

    def get_index_of_best_value_with(self, data, matrix_dimensions_order, join_matrix):

        if join_matrix is None:
            log.critical("Matrice NULL pour la méthode dpop.getIndexOfBestValueWith(...)",
                         self.dfs_structure.monitored_area.id)
            return c.INFINITY_IDX

        if len(join_matrix.shape) == 1 or join_matrix.shape[1] == 1:
            indices = [i for i, x in enumerate(join_matrix) if x == min(join_matrix)]
            return indices[len(indices) - 1]

        if data is None or not isinstance(data, dict):
            log.critical("Données manquantes pour la méthode dpop.getIndexOfBestValueWith(...)",
                         self.dfs_structure.monitored_area.id)
            return c.INFINITY_IDX

        tupl = self.extract_parent_values(data)
        tupl = self.extract_dependant_non_neighbors_values(data, join_matrix, matrix_dimensions_order, tupl)

        return self.find_best_index(join_matrix, tupl)

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

    @staticmethod
    def find_best_index(join_matrix, tupl):

        best_index = 0
        best_value = c.INFINITY + 1

        for index, value in numpy.ndenumerate(join_matrix):
            if tupl == index[1:] and value <= best_value:
                best_value = value
                best_index = index[0]

        return best_index

    @staticmethod
    def extract_dependant_non_neighbors_values(data, join_matrix, matrix_dimensions_order, tupl):
        # Check for dependant non-neighbors values if needed
        for neighbor_id in matrix_dimensions_order:

            if len(join_matrix.shape) - 1 == len(tupl):
                break

            key = str(neighbor_id)
            if key in data:
                tupl = tupl + (data[key],)
        return tupl
