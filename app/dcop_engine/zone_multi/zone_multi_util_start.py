from datetime import datetime

import json
import itertools
import constants as c

from dcop_engine.constraint_manager import *
from dcop_engine.basic_strat.util_strat_abstract import UtilStratAbstract
from logs.message_types import MessageTypes
from logs import log


class ZoneMultiUtilStrat(UtilStratAbstract):

    def __init__(self, mqtt_manager, dfs_structure):
        UtilStratAbstract.__init__(self, mqtt_manager, dfs_structure)
        self.JOIN = []
        self.UTIL = []

    def do_util_propagation(self):

        log.info("Util Start", self.dfs_structure.monitored_area.id, c.INFO)

        if len(self.dfs_structure.children_id) > 0:
            self.get_util_matrix_from_childen()

        if not self.dfs_structure.is_root:

            # Also join all relations with parent/pseudo_parent
            self.JOIN = self.combine(self.get_utility_matrix_for(self.dfs_structure.parent_id), self.JOIN)

            for pseudo_parent in self.dfs_structure.pseudo_parents_id:
                self.JOIN = self.combine(self.get_utility_matrix_for(pseudo_parent), self.JOIN)

        else:
            # Add to `self` constraint values
            self.JOIN = self.get_carthesian_product_list()

        # Use projection to eliminate self out of message parent
        self.UTIL = self.project(self.JOIN)

    def get_util_matrix_from_childen(self):
        count = 0
        start_time = datetime.now()

        # MQTT wait for incoming message of type UTIL for each child of the agent
        while count < len(self.dfs_structure.children_id) and (
                datetime.now() - start_time).total_seconds() < c.TIMEOUT:

            if self.mqtt_manager.has_util_msg():
                # We add to the join UTIL message from children as they arrive
                data_received = json.loads(
                    self.mqtt_manager.client.util_msgs.pop(0).split(MessageTypes.UTIL.value + " ")[1]
                )

                matrix_data = data_received[c.DATA]
                self.JOIN = matrix_data if self.JOIN is None else self.JOIN + matrix_data
                count += 1

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

        arrangement_list = self.get_carthesian_product_list()

        # Adding the parent zone values (neighborhood)
        second_arrangement_list = []
        temp_list = [list(t) for t in itertools.product(["Z" + str(parent_id)], c.DIMENSION)]

        for t in temp_list:
            for element in arrangement_list:

                value = 0

                for sub_element in element:
                    value += c3_neighbors_sync(sub_element[1], t[1])

                second_arrangement_list.append(element + [t + [value]])

        return second_arrangement_list

    def get_carthesian_product_list(self):
        # Get all arrangements values for all room X all dimensions of the current zone ( = pow(nb_dim, nb_rooms))
        vrac_list = []
        for r in self.dfs_structure.monitored_area.rooms:

            temp_list = [list(t) for t in itertools.product(str(r.id), c.DIMENSION)]
            first_arrangement_list = []

            for t in temp_list:
                first_arrangement_list.append(
                    t + [get_cost_of_private_constraints_for_value(r, t[1])]
                )

            vrac_list.append(first_arrangement_list)

        return [list(t) for t in itertools.product(*vrac_list)]

    def combine(self, tuple_list_1, tuple_list_2):

        final_list = []
        nb_rooms = len(self.dfs_structure.monitored_area.rooms)

        if not tuple_list_1 and not tuple_list_2:
            log.critical("List Null and should not be !",
                         self.dfs_structure.monitored_area.id)
            return []

        if not tuple_list_1:
            return tuple_list_2

        if not tuple_list_2:
            return tuple_list_1

        print("size list 1 ", len(tuple_list_1))
        print("size list 2 ", len(tuple_list_2))

        for element in tuple_list_1:
            for second_element in tuple_list_2:

                if element[:nb_rooms] == second_element[:nb_rooms]:
                    final_list.append(
                        element + [second_element[-1]]
                    )
                else:
                    elements_in_double = [
                        x
                        for x in second_element
                        if 'Z' + str(self.dfs_structure.monitored_area.id) in x[0]
                           or x[0] in element[nb_rooms:][0]
                    ]

                    if elements_in_double:
                        final_list.append(
                            element + [
                                x for x in second_element if x not in elements_in_double
                            ]
                        )

        log.info("Shape Combined list : "
                 + str(len(final_list)),
                 self.dfs_structure.monitored_area.id,
                 c.UTIL)

        return final_list

    def project(self, initial_list):
        """
        PROJECT me out of the list
        :param initial_list: list to be projected out
        :type initial_list: list
        :return: a list with one less dimension
        :rtype: list
        """

        if self.dfs_structure.is_root:
            return initial_list

        nb_rooms = len(self.dfs_structure.monitored_area.rooms)
        temp_dict = {}

        for element in initial_list:

            index = sum(element[nb_rooms:], [])[:-1]
            coast = temp_dict.setdefault(tuple(index), sum(e[2] for e in element[:nb_rooms]))
            temp_dict[tuple(index)] = coast + index[1]

        dict_as_list = [list(k) + [v] for k, v in temp_dict.items()]
        dimension_number = int(len(dict_as_list[0]) / 3)
        projected_list = [element[i:i + 3] for element in dict_as_list for i in range(0, len(element), 3)]

        return [projected_list[i:i + dimension_number] for i in range(0, len(projected_list), dimension_number)]
