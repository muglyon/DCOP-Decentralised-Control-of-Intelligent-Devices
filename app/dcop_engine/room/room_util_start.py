from datetime import datetime

import json
import numpy
import time

from dcop_engine.constraint_manager import *
from dcop_engine.basic_strat.util_strat_abstract import UtilStratAbstract
from logs.message_types import MessageTypes
from logs import log


class RoomUtilStrat(UtilStratAbstract):

    def __init__(self, mqtt_manager, dfs_structure):
        UtilStratAbstract.__init__(self, mqtt_manager, dfs_structure)
        self.matrix_dimensions_order = []  # order or the variables that create the JOIN Matrix

    def do_util_propagation(self):

        log.info("Util Start", self.dfs_structure.monitored_area.id, c.INFO)

        if len(self.dfs_structure.children_id) > 0:
            self.get_util_matrix_from_childen()

        if not self.dfs_structure.is_root:

            # Also join all relations with parent/pseudo_parent
            self.JOIN = self.combine(self.get_utility_matrix_for(self.dfs_structure.parent_id), self.JOIN)

            for pseudo_parent in self.dfs_structure.pseudo_parents_id:
                self.JOIN = self.combine(self.get_utility_matrix_for(pseudo_parent), self.JOIN)

        # Add to `self` constraint values
        self.JOIN = self.add_my_utility_in(self.JOIN)

        # Use projection to eliminate self out of message parent
        self.UTIL = self.project(self.JOIN)

    def get_util_matrix_from_childen(self):
        count = 0
        start_time = datetime.now()

        # MQTT wait for incoming message of type UTIL for each child of the agent
        while count < len(self.dfs_structure.children_id) \
                and (datetime.now() - start_time).total_seconds() < c.TIMEOUT:
            if self.mqtt_manager.has_util_msg():
                # We add to the join UTIL message from children as they arrive
                data_received = json.loads(
                    self.mqtt_manager.client.util_msgs.pop(0).split(MessageTypes.UTIL.value + " ")[1]
                )

                matrix_data = numpy.asarray(data_received[c.DATA])
                self.matrix_dimensions_order.extend(data_received[c.VARS])
                self.JOIN = matrix_data if self.JOIN is None else self.JOIN + matrix_data
                count += 1

                self.matrix_dimensions_order = list(set(self.matrix_dimensions_order))  # Clean up duplicate entry
            else:
                time.sleep(0.01)

    def get_utility_matrix_for(self, parent_id):
        """
        Generate the R matrix depending on parent
        :param parent_id: id of my parent
        :type parent_id: integer
        :return: the utility matrix R
        :rtype: numpy.ndarray
        """
        R = numpy.zeros((c.DIMENSION_SIZE, c.DIMENSION_SIZE), int)

        if parent_id in self.matrix_dimensions_order:
            # Parent was already take in account by one of my children
            return None

        for i in range(0, c.DIMENSION_SIZE):
            for j in range(0, c.DIMENSION_SIZE):
                R[i][j] += c3_neighbors_sync(c.DIMENSION[i], c.DIMENSION[j])

        self.matrix_dimensions_order.append(parent_id)
        return R

    def combine(self, matrix1, matrix2):
        """
        JOIN/COMBINE two matrix
        :type matrix1: numpy.ndarray
        :type matrix2: numpy.ndarray
        :return: combined matrix
        :rtype: numpy.ndarray
        """

        if matrix1 is None and matrix2 is None:
            log.critical("Matrices Null and should not be !",
                         self.dfs_structure.monitored_area.id)
            return numpy.zeros(c.DIMENSION_SIZE, int)

        if matrix1 is None:
            return matrix2

        if matrix2 is None:
            return matrix1

        if matrix1.size > matrix2.size:
            final_matrix = numpy.zeros(matrix1.shape + (matrix1.shape[0],), int)
        else:
            final_matrix = numpy.zeros(matrix2.shape + (matrix2.shape[0],), int)

        for index1, value1 in numpy.ndenumerate(matrix1):
            for index2, value2 in numpy.ndenumerate(matrix2):
                if index1[0] == index2[0]:
                    tupl = tuple(numpy.concatenate((numpy.array(index1), numpy.delete(numpy.array(index2), 0, 0))))
                    final_matrix[tupl] = value1 + value2

        log.info("Shape Combined matrix : " + str(final_matrix.shape),
                 self.dfs_structure.monitored_area.id,
                 c.UTIL)

        return final_matrix

    def add_my_utility_in(self, R):
        """
        Add my utility in the matrix.
        This is needed because I am the only one to know those constraints
        :param R: the matrix that will receive my utilities values
        :type R: numpy.ndarray
        :return: the new matrix
        :rtype: numpy.ndarray
        """
        if R is None:
            R = numpy.zeros(c.DIMENSION_SIZE, int)

        for index, value in numpy.ndenumerate(R):
            R[index] += get_cost_of_private_constraints_for_value(
                self.dfs_structure.monitored_area, c.DIMENSION[index[0]]
            )

            if R[index] > c.INFINITY:
                R[index] = c.INFINITY

        return R

    @staticmethod
    def project(matrix):
        """
        PROJECT me out of the matrix
        :param matrix: matrix to be projected out
        :type matrix: numpy.ndarray
        :return: a matrix with one less dimension
        :rtype: numpy.ndarray
        """
        return numpy.amin(matrix, axis=0) if len(matrix.shape) > 1 else matrix
