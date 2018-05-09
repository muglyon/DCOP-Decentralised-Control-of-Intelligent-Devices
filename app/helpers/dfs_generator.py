#! python3
from helpers.message_types import MessageTypes


class DfsGenerator(object):

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

        # Root Election
        self.mqtt_manager.publish_root_msg()

        while len(self.mqtt_manager.mqtt_client.list_msgs_waiting) == 0:
            # Wait for Root choice
            pass

        if int(self.mqtt_manager.mqtt_client.list_msgs_waiting.pop(0).split("_")[1]) == self.room.id:
            self.is_root = True

        if self.room.get_degree() > 0:

            if self.is_root:
                self.open_neighbors_id = self.room.get_neighbors_id_sorted()
                self.children_id.append(self.open_neighbors_id.pop(0))
                self.mqtt_manager.publish_child_msg_to(self.children_id[0])

            # MQTT wait for incoming message of type "messageType" from neighbor yi
            while 1:

                if len(self.mqtt_manager.mqtt_client.child_msgs) == 0:
                    continue

                message = self.mqtt_manager.mqtt_client.child_msgs.pop(0).split(" ")
                message_type = message[0]
                yi = int(message[1])

                if self.open_neighbors_id is None:
                    # First time the agent is visited
                    self.open_neighbors_id = self.room.get_neighbors_id_sorted_except(yi)
                    self.parent_id = yi

                elif message_type == MessageTypes.CHILD.value and yi in self.open_neighbors_id:
                    self.pseudo_children_id.append(self.open_neighbors_id.pop(self.open_neighbors_id.index(yi)))
                    self.mqtt_manager.publish_pseudo_msg_to(yi)
                    continue

                elif message_type == MessageTypes.PSEUDO.value:
                    if yi in self.children_id:
                        self.children_id.pop(self.children_id.index(yi))
                    self.pseudo_parents_id.append(yi)

                # Forward the CHILD message to the next "open" neighbor
                if len(self.open_neighbors_id) > 0:
                    yj = self.open_neighbors_id[0]
                    self.children_id.append(self.open_neighbors_id.pop(0))
                    self.mqtt_manager.publish_child_msg_to(yj)
                else:
                    if not self.is_root:
                        # Backtrack
                        self.mqtt_manager.publish_child_msg_to(self.parent_id)

                    print(self.pseudo_tree_to_string())
                    return

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
