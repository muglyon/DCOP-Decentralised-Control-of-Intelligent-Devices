from threads.starter import Starter


class UrgentStarter(Starter):

    def __init__(self, agents, mqtt_client, critical_root_chosen=0):
        Starter.__init__(self, agents, mqtt_client)

        self.critical_root_chosen = critical_root_chosen

    def run(self):
        self.do_one_iteration()

    def choose_root(self):

        if self.critical_root_chosen > 0:

            root = self.critical_root_chosen
            self.critical_root_chosen = 0
            return root

        return super().choose_root()
