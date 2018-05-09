#! python3
from helpers.message_types import MessageTypes


class DfsManager(object):

    def __init__(self, mqtt_manager, room):
        self.mqtt_manager = mqtt_manager
        self.room = room
        self.is_root = False

        self.open_neighbors_id = None  # neighbors Id : see "open" in the algorithm
        self.children_id = []
        self.parent_id = 0
        self.pseudo_children_id = []
        self.pseudo_parents_id = []

    def create_pseudo_tree(self):

        print("\n---------- DFS GENERATION ----------")

        self.root_selection()

        if self.room.get_degree() > 0:

            if self.is_root:
                self.open_neighbors_id = self.room.get_neighbors_id_sorted()
                self.children_id.append(self.open_neighbors_id.pop(0))
                self.mqtt_manager.publish_child_msg_to(self.children_id[0])

            # MQTT wait for incoming message of type "messageType" from neighbor yi
            while 1:

                if self.mqtt_manager.has_no_child_msg():
                    continue

                message = self.mqtt_manager.client.child_msgs.pop(0).split(" ")
                message_type = message[0]
                yi = int(message[1])

                if self.open_neighbors_id is None:
                    # First time the agent is visited
                    self.open_neighbors_id = self.room.get_neighbors_id_sorted_except(yi)
                    self.parent_id = yi

                elif MessageTypes.is_child(message_type) and yi in self.open_neighbors_id:
                    self.pseudo_children_id.append(self.open_neighbors_id.pop(self.open_neighbors_id.index(yi)))
                    self.mqtt_manager.publish_pseudo_msg_to(yi)
                    continue

                elif MessageTypes.is_pseudo(message_type):
                    if yi in self.children_id:
                        self.children_id.pop(self.children_id.index(yi))
                    self.pseudo_parents_id.append(yi)

                # Forward the CHILD message to the next "open" neighbor
                if len(self.open_neighbors_id) > 0:
                    yj = self.open_neighbors_id[0]
                    self.children_id.append(self.open_neighbors_id.pop(0))
                    self.mqtt_manager.publish_child_msg_to(yj)
                else:

                    if self.is_root:
                        pass
                    else:
                        # Backtrack
                        self.mqtt_manager.publish_child_msg_to(self.parent_id)

                    print(self.pseudo_tree_to_string())
                    return

    def root_selection(self):

        self.mqtt_manager.publish_root_value_msg()

        while self.mqtt_manager.has_no_msg():
            # Wait for Root choice from server
            pass

        self.is_root = self.i_am_the_elected_root()

    def i_am_the_elected_root(self):
        return int(self.mqtt_manager.client.list_msgs_waiting.pop(0).split("_")[1]) == self.room.id

    def is_leaf(self):
        return len(self.children_id) == 0

    def pseudo_tree_to_string(self):
        """
        Convert PSEUDO-Tree in String Format
        :return: pseudo-tree in string format
        :rtype: string
        """
        string = str(self.room.id) + "\n"

        for childId in self.children_id:
            string += "| " + str(childId) + "\n"

        for pseudoId in self.pseudo_parents_id:
            string += "--> " + str(pseudoId) + "\n"

        for pseudoId in self.pseudo_children_id:
            string += "<-- " + str(pseudoId) + "\n"

        return string
