#! python3
from helpers.managers.dpop_manager import DpopManager
from helpers.message_types import MessageTypes
from model.dfs_structure import DfsStructure


class DfsManager(DpopManager):

    def __init__(self, mqtt_manager, room):
        DpopManager.__init__(self,mqtt_manager, DfsStructure(room))

    def generate_dfs(self):

        print("\n---------- DFS GENERATION ----------")

        self.choose_root()

        if self.dfs_structure.room.get_degree() > 0:

            if self.dfs_structure.is_root:
                self.dfs_structure.open_neighbors_id = self.dfs_structure.room.get_neighbors_id_sorted()
                self.dfs_structure.children_id.append(self.dfs_structure.open_neighbors_id.pop(0))
                self.mqtt_manager.publish_child_msg_to(self.dfs_structure.children_id[0])

            self.generate_dfs_with_others_agents()

    def generate_dfs_with_others_agents(self):

        continue_generation = True
        while continue_generation:

            # MQTT wait for incoming message of type "message_type" from neighbor yi
            if self.mqtt_manager.has_child_msg():

                message = self.mqtt_manager.client.child_msgs.pop(0).split(" ")
                message_type = message[0]
                yi = int(message[1])

                if self.dfs_structure.open_neighbors_id is None:
                    # First time the agent is visited
                    self.dfs_structure.open_neighbors_id = self.dfs_structure.room.get_neighbors_id_sorted_except(yi)
                    self.dfs_structure.parent_id = yi

                elif MessageTypes.is_child(message_type) and yi in self.dfs_structure.open_neighbors_id:
                    self.dfs_structure.pseudo_children_id.append(
                        self.dfs_structure.open_neighbors_id.pop(self.dfs_structure.open_neighbors_id.index(yi))
                    )
                    self.mqtt_manager.publish_pseudo_msg_to(yi)
                    continue

                elif MessageTypes.is_pseudo(message_type):
                    if yi in self.dfs_structure.children_id:
                        self.dfs_structure.children_id.pop(self.dfs_structure.children_id.index(yi))
                    self.dfs_structure.pseudo_parents_id.append(yi)

                # Forward the CHILD message to the next "open" neighbor
                if len(self.dfs_structure.open_neighbors_id) > 0:
                    yj = self.dfs_structure.open_neighbors_id[0]
                    self.dfs_structure.children_id.append(self.dfs_structure.open_neighbors_id.pop(0))
                    self.mqtt_manager.publish_child_msg_to(yj)
                else:

                    if self.dfs_structure.is_root:
                        pass
                    else:
                        # Backtrack
                        self.mqtt_manager.publish_child_msg_to(self.dfs_structure.parent_id)

                    print(self.pseudo_tree_to_string())
                    continue_generation = False

    def choose_root(self):

        self.mqtt_manager.publish_root_value_msg()

        while self.mqtt_manager.has_no_msg():
            # Wait for Root choice from server
            pass

        self.dfs_structure.is_root = self.am_i_the_elected_root()

    def am_i_the_elected_root(self):
        return int(self.mqtt_manager.client.list_msgs_waiting.pop(0).split("_")[1]) == self.dfs_structure.room.id

    def pseudo_tree_to_string(self):
        """
        Convert PSEUDO-Tree in String Format
        :return: pseudo-tree in string format
        :rtype: string
        """
        string = str(self.dfs_structure.room.id) + "\n"

        for childId in self.dfs_structure.children_id:
            string += "| " + str(childId) + "\n"

        for pseudoId in self.dfs_structure.pseudo_parents_id:
            string += "--> " + str(pseudoId) + "\n"

        for pseudoId in self.dfs_structure.pseudo_children_id:
            string += "<-- " + str(pseudoId) + "\n"

        return string
