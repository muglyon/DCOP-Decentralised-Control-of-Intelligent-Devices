#! python3
# starter.py - Thread which gives "TOP" to the DPOP agents
# It is a thread intended to be launched by the server
import operator
import constants as c

from dcop_server.starter import Starter


class StarterZoneMulti(Starter):

    def __init__(self, agents, mqtt_client):
        Starter.__init__(self, agents, mqtt_client)

    def get_result_by_priority(self, received_values):

        results = ""
        for key in received_values:

            if received_values[key] < c.URGT_TIME:
                if self.old_results_index[key.split("Z")[1]] <= c.URGT_TIME:
                    self.priorities[key.split("Z")[1]] += 1
            else:
                self.priorities[key.split("Z")[1]] = 0

        sorted_priorities = sorted(self.priorities.items(), key=operator.itemgetter(1), reverse=True)

        for agent_id, priority in sorted_priorities:
            results += "Monitoring Area " + str(agent_id) + \
                       " need intervention in " + str(received_values["Z" + str(agent_id)]) + \
                       " minutes. PRIORITY : " + str(priority) + " "
            self.old_results_index["Z" + str(agent_id)] = received_values["Z" + str(agent_id)]

        return results
