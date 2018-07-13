from datetime import datetime

import json
import numpy
import itertools

from constants import Constants
from dcop_engine.constraint_manager import ConstraintManager
from dcop_engine.managers.dpop_manager import DpopManager
from logs.message_types import MessageTypes
from logs import log


class UtilManager(DpopManager):

    def __init__(self, mqtt_manager, dfs_structure):
        DpopManager.__init__(self, mqtt_manager, dfs_structure)

        self.JOIN = []
        self.UTIL = []
        self.constraint_manager = ConstraintManager()

        # Todo : no need for that ?
        # self.matrix_dimensions_order = []  # order or the variables that create the JOIN Matrix

    def do_util_propagation(self):
        log.info("Util Start", self.dfs_structure.monitored_area.id, Constants.INFO)

        if len(self.dfs_structure.children_id) > 0:
            self.get_util_matrix_from_childen()

        if not self.dfs_structure.is_root:

            # Also join all relations with parent/pseudo_parent
            self.JOIN = self.combine(self.get_utility_matrix_for(self.dfs_structure.parent_id), self.JOIN)

            for pseudo_parent in self.dfs_structure.pseudo_parents_id:
                self.JOIN = self.combine(self.get_utility_matrix_for(pseudo_parent), self.JOIN)

        else:
            # Add to `self` constraint values
            self.JOIN = self.add_my_utility_in(self.JOIN)

        print("JOIN before projection :", self.JOIN)

        # Use projection to eliminate self out of message parent
        self.UTIL = self.project(self.JOIN)

        print("UTIL after projection :", self.UTIL)

    def get_util_matrix_from_childen(self):
        count = 0
        start_time = datetime.now()

        # MQTT wait for incoming message of type UTIL for each child of the agent
        while count < len(self.dfs_structure.children_id) \
                and (datetime.now() - start_time).total_seconds() < Constants.TIMEOUT:

            if self.mqtt_manager.has_util_msg():
                # We add to the join UTIL message from children as they arrive
                data_received = json.loads(
                    self.mqtt_manager.client.util_msgs.pop(0).split(MessageTypes.UTIL.value + " ")[1]
                )

                matrix_data = data_received[Constants.DATA]
                # Todo : no need for that ?
                # self.matrix_dimensions_order.extend(data_received[Constants.VARS])
                self.JOIN = matrix_data if self.JOIN is None else self.JOIN + matrix_data
                count += 1
                #
                # self.matrix_dimensions_order = list(set(self.matrix_dimensions_order))  # Clean up duplicate entry

    def get_utility_matrix_for(self, parent_id):
        """
        Generate the R matrix depending on parent
        :param parent_id: id of my parent
        :type parent_id: integer
        :return: the utility matrix R
        :rtype: list
        """

        if 'Z' + str(parent_id) in self.JOIN:
            # Parent was already take in account by one of my children
            return None

        R, arrangement_list = self.get_carthesian_product_list()

        # Todo : rajouter la contrainte de voisinage inter-chambre ?
        # Adding the parent zone values (neighborhood)

        temp_list = [list(t) for t in itertools.product(["Z" + str(parent_id)], Constants.DIMENSION)]
        r_list_2 = []

        for t in temp_list:
            for element in arrangement_list:

                value = 0

                for sub_element in element:
                    value += self.constraint_manager.c3_neighbors_sync(sub_element[1], t[1])

                r_list_2.append(element + [t + [value]])

        R.append(r_list_2)
        print("step 2 ", r_list_2)

        # self.matrix_dimensions_order.append(parent_id)

        return r_list_2

    def get_carthesian_product_list(self):
        # Get all arrangements values for all room X all dimensions of the current zone ( = pow(nb_dim, nb_rooms))
        R = []

        for r in self.dfs_structure.monitored_area.rooms:

            temp_list = [list(t) for t in itertools.product(str(r.id), Constants.DIMENSION)]
            r_list_1 = []

            print("step -1 ", temp_list)

            for t in temp_list:
                r_list_1.append(t + [self.constraint_manager.get_cost_of_private_constraints_for_value(r, t[1])])

            R.append(r_list_1)

        print("step 0 ", R)

        arrangement_list = R[0]
        for i in range(1, len(R)):
            arrangement_list = [list(t) for t in itertools.product(arrangement_list, R[i])]

        print("step 1 ", arrangement_list)

        return R, arrangement_list

    def combine(self, tuple_list_1, tuple_list_2):
        """
        JOIN/COMBINE two tuple list
        :type tuple_list_1: list
        :type tuple_list_2: list
        :return: combined list
        :rtype: list
        """

        final_list = []

        print("list 1 : ", tuple_list_1)
        print("list 2 : ", tuple_list_2)

        if not tuple_list_1 and not tuple_list_2:
            log.critical("List Null and should not be !",
                         self.dfs_structure.monitored_area.id)
            return []

        if not tuple_list_1:
            return tuple_list_2

        if not tuple_list_2:
            return tuple_list_1

        for element in tuple_list_1:
            for second_element in tuple_list_2:

                print("e1 ",  element[:-1])
                print("e2 ", second_element[:-1])

                if element[:-1] == second_element[:-1]:
                    final_list.append(
                        element[:-1]
                        + [element[len(element) - 1]]
                        + [second_element[len(second_element) - 1]]
                    )

        print("Combined list ", final_list)

        log.info("Shape Combined list : "
                 + str(len(final_list))
                 + " And expected : "
                 + str(pow(Constants.DIMENSION_SIZE, len(self.dfs_structure.monitored_area.rooms) + 2)),
                 self.dfs_structure.monitored_area.id,
                 Constants.UTIL)

        return final_list


    def add_my_utility_in(self, R):
        # Todo : remove ?
        # if R is None:
        #     R = numpy.zeros(Constants.DIMENSION_SIZE, int)
        #
        # for index, value in numpy.ndenumerate(R):
        #     R[index] += self.constraint_manager.get_cost_of_private_constraints_for_value(Constants.DIMENSION[index[0]])
        #
        #     if R[index] > Constants.INFINITY:
        #         R[index] = Constants.INFINITY
        #
        # return R
        R, arrangement_list = self.get_carthesian_product_list()
        print("Add my utility : ", arrangement_list)
        return arrangement_list

    def project(self, list):
        """
        PROJECT me out of the list
        :param list: list to be projected out
        :type list: list
        :return: a matrix with one less dimension
        :rtype: list
        """

        new_list = []
        print("LIST : ", list)

        if 'Z' in list:
            return list

        nb_rooms = len(self.dfs_structure.monitored_area.rooms)

        for element in list:

            size = len(element[-nb_rooms:])
            new_list.append(element[-nb_rooms:])

            print(new_list[len(new_list) - 1][0])
            print(new_list[len(new_list) - 1][0][2])
            print(element[:-size])
            print(sum([e[2] for e in element[:-size]]))

            new_list[len(new_list) - 1][0][2] += sum([e[2] for e in element[:-size]])

        return new_list

