#! python3
# dpop.py - Implement the DPOP Algorithm
# It is a thread intended to be launched by an agent
#
# /!\ WARNING /!\
# The objective in this case is to MINIMIZE all constraints.

from threading import Thread
from datetime import datetime
from helpers.dfsGenerator import DfsGenerator
from helpers.constraintManager import ConstraintManager
from helpers.mqtt_manager import MqttManager

import numpy
import json


class Dpop(Thread):

    DIMENSION = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120, 180, 210, 241]
    DIMENSION_SIZE = len(DIMENSION)
    INFINITY = 241
    TIMEOUT = 200

    def __init__(self, room, mqtt_client):
        Thread.__init__(self)
        self.room = room
        self.is_root = False

        self.matrix_dimensions = []  # order or the variables that create the JOIN Matrix
        self.UTIL = None  # UTIL matrix
        self.JOIN = None  # JOIN matrix

        self.constraint_manager = ConstraintManager(self.room)
        self.mqtt_manager = MqttManager(mqtt_client, self.room)
        self.dfs_generator = DfsGenerator(self.mqtt_manager, self.room)

    def run(self):
        """
        /!\ Do the DPOP Algorithm /!\
        """
        self.dfs_generator.create_pseudo_tree()
        self.util_propagation()
        self.value_propagation()

    def util_propagation(self):
        """
        UTIL Propagation phase
        """

        print("\n---------- UTIL PROPAGATION ----------")

        count = 0
        start_time = datetime.now()
        
        if len(self.dfs_generator.children) > 0:
           
            # MQTT wait for incoming message of type UTIL for each child of the agent
            while count < len(self.dfs_generator.children) \
                    and (datetime.now() - start_time).total_seconds() < self.TIMEOUT:
                
                if len(self.mqtt_manager.mqtt_client.util_msgs) == 0:
                    continue
                
                # We add to the join UTIL message from children as they arrive
                data_received = json.loads(self.mqtt_manager.mqtt_client.util_msgs.pop(0).split("UTIL ")[1])
                self.matrix_dimensions.extend(data_received["vars"])
                matrix_data = numpy.asarray(data_received["data"]) 
                self.JOIN = matrix_data if self.JOIN is None else self.JOIN + matrix_data
                count += 1

                self.matrix_dimensions = list(set(self.matrix_dimensions))  # Clean up duplicate entry

        if not self.is_root:

            # Also join all relations with parent/pseudo_parent
            self.JOIN = self.combine(self.get_utility_matrix_for(self.dfs_generator.parent_id), self.JOIN)
        
            for pseudo_parent in self.dfs_generator.pseudo_parent:
                self.JOIN = self.combine(self.get_utility_matrix_for(pseudo_parent), self.JOIN)

        # Add to `self` constraint values
        self.JOIN = self.add_my_utility_in(self.JOIN)

        # Use projection to eliminate self out of message parent
        self.UTIL = self.project(self.JOIN)

    def value_propagation(self):
        """
        VALUE Propagation phase
        """

        print("\n---------- VALUE PROPAGATION ----------")

        values = {}
        start_time = datetime.now()

        if self.UTIL is None:
            self.UTIL = numpy.zeros(self.DIMENSION_SIZE, int)

        if not self.is_root:

            self.mqtt_manager.publish_util_msg_to(self.dfs_generator.parent_id,
                                                  json.dumps({"vars": self.matrix_dimensions, "data": self.UTIL.tolist()}))

            # MQTT wait for incoming message of type VALUE from parent
            while (datetime.now() - start_time).total_seconds() < self.TIMEOUT:

                if len(self.mqtt_manager.mqtt_client.value_msgs) == 0:
                    continue

                values = json.loads(self.mqtt_manager.mqtt_client.value_msgs.pop(0).split("VALUES ")[1])
                break

        # Find best v
        index = self.get_index_of_best_value_with(values)
        self.room.current_v = self.DIMENSION[index]
        values[str(self.room.id)] = index

        for child in self.dfs_generator.children:
            self.mqtt_manager.publish_value_msg_to(child, json.dumps(values))

        if len(self.dfs_generator.children) == 0:
            self.mqtt_manager.publish_value_msg_to_server(json.dumps(values))

        print("FINAL v : " + str(self.room.current_v))
        print("const vals : ", self.constraint_manager.get_value_of_private_constraints_for_value(self.room.current_v))

    '''''''''''''''''''''''''''''''''''''''''''''''''''
              METHODS UTILS                      
    '''''''''''''''''''''''''''''''''''''''''''''''''''

    def get_index_of_best_value_with(self, data):
        """
        Find index of best value for me depending on the other values
        :param data: data received by mqtt
        :type data: json object
        :return: index corresponding to best value for me in DIMENSION
        :rtype: integer
        """

        if self.JOIN is None:
            raise Exception("Matrice NULL pour la méthode dpop.getIndexOfBestValueWith(...)")

        if len(self.JOIN.shape) == 1 or self.JOIN.shape[1] == 1:
            indices = [i for i, x in enumerate(self.JOIN) if x == min(self.JOIN)]
            return indices[len(indices) - 1]

        if data is None or not type(data) is dict:
            raise Exception("Données manquantes pour la méthode dpop.getIndexOfBestValueWith(...)")

        best_value = self.INFINITY + 1
        best_index = 0
        tupl = tuple()

        parents = self.dfs_generator.pseudo_parent
        parents.append(self.dfs_generator.parent_id)

        # Check for parents values
        for parent_id in parents:
            key = str(parent_id)
            if key in data:
                tupl = tupl + (data[key],)

        # Check for dependant non-neighbors values if needed
        for neighbor_id in self.matrix_dimensions:

            if len(self.JOIN.shape) - 1 == len(tupl):
                break

            key = str(neighbor_id)
            if key in data:
                tupl = tupl + (data[key],)

        for index, value in numpy.ndenumerate(self.JOIN):
            if tupl == index[1:]:

                if value <= best_value:
                    best_value = value
                    best_index = index[0]

        return best_index

    def project(self, matrix):
        """
        PROJECT me out of the matrix
        :param matrix: matrix to be projected out
        :type matrix: numpy.ndarray
        :return: a matrix with one less dimension
        :rtype: numpy.ndarray
        """
        return numpy.amin(matrix, axis=0) if len(matrix.shape) > 1 else matrix

    def combine(self, matrix1, matrix2):
        """
        JOIN/COMBINE two matrix
        :type matrix1: numpy.ndarray
        :type matrix2: numpy.ndarray
        :return: combined matrix
        :rtype: numpy.ndarray
        """

        if matrix1 is None and matrix2 is None:
            raise Exception("Matrices Null !")

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

        print("SHAPE OF COMBINED MATRIX : " + str(final_matrix.shape))
        return final_matrix

    def get_utility_matrix_for(self, parent_id):
        """
        Generate the R matrix depending on parent
        :param parent_id: id of my parent
        :type parent_id: integer
        :return: the utility matrix R
        :rtype: numpy.ndarray
        """
        R = numpy.zeros((self.DIMENSION_SIZE, self.DIMENSION_SIZE), int)

        if parent_id in self.matrix_dimensions:
            # Parent was already take in account by one of my children
            return None

        for i in range(0, self.DIMENSION_SIZE):
            for j in range(0, self.DIMENSION_SIZE):
                R[i][j] += self.constraint_manager.c3(self.DIMENSION[i], self.DIMENSION[j])

        self.matrix_dimensions.append(parent_id)
        return R

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
            R = numpy.zeros(self.DIMENSION_SIZE, int)
        
        for index, value in numpy.ndenumerate(R):
            R[index] += self.constraint_manager.get_value_of_private_constraints_for_value(self.DIMENSION[index[0]])

            if R[index] == self.INFINITY:
                R[index] = self.INFINITY

        return R
