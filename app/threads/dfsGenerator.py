#! python3


class DfsGenerator(object):

    def __init__(self, mqtt_client, room):
        self.mqtt_client = mqtt_client
        self.room = room
        self.is_root = False

        self.open = None  # neighbors Id
        self.children = []  # children Id
        self.parent_id = 0  # parent Id
        self.pseudo_children = []  # pseudo_children Id
        self.pseudo_parent = []  # pseudo_parents Id

    def create_pseudo_tree(self):

        print("\n---------- DFS GENERATION ----------")

        # Root Election
        self.publish_msg_to_recipient("SERVER", 0)

        print("wait for ROOT")
        while len(self.mqtt_client.list_msgs_waiting) == 0:
            # Wait for Root choice
            pass

        if int(self.mqtt_client.list_msgs_waiting.pop(0).split("_")[1]) == self.room.id:
            self.is_root = True

        if self.room.get_degree() > 0:

            if self.is_root:
                self.open = self.room.get_neighbors_id_sorted()
                self.children.append(self.open.pop(0))
                self.publish_msg_to_recipient("CHILD", self.children[0])

            # MQTT wait for incoming message of type "messageType" from neighbor yi
            while 1:

                if len(self.mqtt_client.child_msgs) == 0:
                    continue

                message = self.mqtt_client.child_msgs.pop(0).split(" ")
                message_type = message[0]
                yi = int(message[1])

                if self.open is None:
                    # First time the agent is visited
                    self.open = self.room.get_neighbors_id_sorted_except(yi)
                    self.parent_id = yi

                elif "CHILD" in message_type and yi in self.open:
                    self.pseudo_children.append(self.open.pop(self.open.index(yi)))
                    self.publish_msg_to_recipient("PSEUDO", yi)
                    continue

                elif "PSEUDO" in message_type:
                    if yi in self.children:
                        self.children.pop(self.children.index(yi))
                    self.pseudo_parent.append(yi)

                # Forward the CHILD message to the next "open" neighbor
                if len(self.open) > 0:
                    yj = self.open[0]
                    self.children.append(self.open.pop(0))
                    self.publish_msg_to_recipient("CHILD", yj)
                else:
                    if not self.is_root:
                        # Backtrack
                        self.publish_msg_to_recipient("CHILD", self.parent_id)

                    print(self.pseudo_tree_to_string())
                    return

    def publish_msg_to_recipient(self, msg_type, recipient_id):
        """
        Publish a <msg_type> message in the <recipient_id> topic with mqtt
        :param msg_type: 'CHILD', 'UTIL', etc...
        :type msg_type: string
        :param recipient_id: id of the recipient agent
        :type recipient_id: integer
        """
        if msg_type is "SERVER":
            self.mqtt_client.publish("DCOP/SERVER/ROOT", str(self.room.id) + ":" + str(self.room.get_degree()))
        if msg_type is "CHILD":
            self.mqtt_client.publish("DCOP/" + str(recipient_id), "CHILD " + str(self.room.id))
        elif msg_type is "PSEUDO":
            self.mqtt_client.publish("DCOP/" + str(recipient_id), "PSEUDO " + str(self.room.id))

    def pseudo_tree_to_string(self):
        """
        Convert PSEUDO-Tree in String Format
        :return: pseudo-tree in string format
        :rtype: string
        """
        string = str(self.room.id) + "\n"

        for childId in self.children:
            string += "| " + str(childId) + "\n"

        for pseudoId in self.pseudo_parent:
            string += "--> " + str(pseudoId) + "\n"

        for pseudoId in self.pseudo_children:
            string += "<-- " + str(pseudoId) + "\n"

        return string
